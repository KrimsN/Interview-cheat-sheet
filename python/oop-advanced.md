# ООП вглубь: MRO, дескрипторы, `__slots__`, метаклассы

[← Пример: bound methods](bound-methods-example.md) · [🏠 Домой](../README.md) · [Управление памятью →](memory-management.md)

---

## Что такое MRO и как на самом деле работает `super()`?

**Коротко.** MRO (Method Resolution Order) — линейный порядок классов, в котором
ищется атрибут. Строится алгоритмом C3-линеаризации. `super()` не «вызывает
родителя», а передаёт управление **следующему классу в MRO текущего объекта** —
и этот класс может вообще не быть предком того, где написан `super()`.

```python
class A:
    def who(self): return "A"
class B(A):
    def who(self): return "B->" + super().who()
class C(A):
    def who(self): return "C->" + super().who()
class D(B, C):
    def who(self): return "D->" + super().who()

[c.__name__ for c in D.__mro__]
# ['D', 'B', 'C', 'A', 'object']
D().who()
# 'D->B->C->A'
```

Это ответ на diamond problem: `A` вызывается **один раз**, а `super()` внутри
`B` уходит в `C`, хотя `C` не является родителем `B`. Правила C3: сам класс
идёт первым, порядок базовых классов сохраняется, и каждый класс появляется
после всех своих потомков.

**Подвох.** Не любую иерархию можно линеаризовать — противоречивый порядок
баз падает ещё на объявлении класса:

```python
class Bad(A, B): ...
# TypeError: Cannot create a consistent method resolution order (MRO)
# for bases A, B
```

`B` — потомок `A`, значит должен идти раньше, но в списке баз он записан
позже. Отсюда практическое правило: базовые классы перечисляют от частного
к общему.

**Глубже.** Из «`super()` идёт по MRO экземпляра» следует требование
кооперативного наследования: сигнатуры методов по цепочке должны быть
совместимы, и `super().__init__(**kwargs)` вызывают все классы в цепочке,
а не только те, у кого «есть родитель». Посмотреть цепочку — `D.__mro__`
или `D.mro()`.

---

## Что такое дескриптор и чем data-дескриптор отличается от non-data?

**Коротко.** Дескриптор — объект с методом `__get__` (и, возможно,
`__set__`/`__delete__`), лежащий в классе как атрибут. Если есть `__set__`
или `__delete__` — это data-дескриптор, и он **приоритетнее** `__dict__`
экземпляра; если только `__get__` — non-data, и его перекрывает запись
в экземпляр.

```python
class Positive:
    def __set_name__(self, owner, name):
        self.name = "_" + name          # имя поля, куда прячем значение
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self                 # обращение через класс
        return getattr(obj, self.name)
    def __set__(self, obj, value):
        if value < 0:
            raise ValueError("must be >= 0")
        setattr(obj, self.name, value)

class Account:
    balance = Positive()
    def __init__(self, b):
        self.balance = b                # уже проходит через __set__

a = Account(10)
a.balance, a.__dict__
# (10, {'_balance': 10})
a.balance = -1
# ValueError: must be >= 0
```

Разница видна на non-data дескрипторе — его легко «затереть»:

```python
class NonData:
    def __get__(self, obj, objtype=None): return "from descriptor"

class Q:
    x = NonData()

q = Q()
q.x                             # from descriptor
q.x = "from instance"
q.x                             # from instance — non-data проиграл
```

Полный порядок поиска `obj.attr`: data-дескриптор в классе → `obj.__dict__` →
non-data дескриптор или обычный атрибут класса → `__getattr__`.

**Подвох.** Именно поэтому обычный метод (у функции есть только `__get__`,
это non-data дескриптор) можно подменить у конкретного экземпляра,
а `property` (data-дескриптор) — нельзя: присваивание уйдёт в её сеттер,
а без сеттера даст `AttributeError`.

**Глубже.** На дескрипторах построены `property`, `classmethod`,
`staticmethod`, `functools.cached_property`, поля `dataclass` со значениями по
умолчанию и ORM-модели. Ручная реализация первых трёх разобрана в
[примере с bound methods](bound-methods-example.md). Метод `__set_name__`
(Python 3.6+) вызывается при создании класса и избавляет от дублирования
имени поля в конструкторе дескриптора.

---

## Что даёт `__slots__` и чем за это платят?

**Коротко.** `__slots__` фиксирует набор атрибутов экземпляра: вместо
`__dict__` создаются слоты-дескрипторы с фиксированными смещениями. Экономия
памяти в разы плюс чуть более быстрый доступ.

```python
import sys

class WithDict:
    def __init__(self): self.a, self.b = 1, 2

class WithSlots:
    __slots__ = ("a", "b")
    def __init__(self): self.a, self.b = 1, 2

d = WithDict()
sys.getsizeof(d) + sys.getsizeof(d.__dict__)   # 344 байта
sys.getsizeof(WithSlots())                     # 48 байт
```

Плата:

- нельзя добавить атрибут, которого нет в `__slots__`;
- нет `__dict__`, значит не работает `vars(obj)` и код, который его ждёт;
- нет `__weakref__`, если не добавить его в `__slots__` явно;
- при множественном наследовании нельзя объединить два класса
  с непустыми `__slots__`;
- достаточно одному классу в цепочке не объявить `__slots__` — и `__dict__`
  вернётся, а экономия пропадёт.

```python
s = WithSlots()
s.c = 3
# AttributeError: WithSlots object has no attribute c
# and no __dict__ for setting new attributes
```

**Подвох.** `__slots__` — оптимизация под **много экземпляров** (миллионы
точек, строк лога, узлов графа). На классе, у которого будет пять объектов,
это лишь ограничение без выгоды. Готовая форма — `@dataclass(slots=True)`
(см. [Классы](classes-dataclasses-enum.md)).

---

## Зачем нужны метаклассы?

**Коротко.** Метакласс — класс, экземплярами которого являются классы. По
умолчанию это `type`. Кастомный метакласс перехватывает **создание класса**:
регистрация плагинов, валидация объявления, автоподстановка атрибутов.

```python
registry = {}

class PluginMeta(type):
    def __new__(mcls, name, bases, ns):
        cls = super().__new__(mcls, name, bases, ns)
        if bases:                      # сам Plugin не регистрируем
            registry[name] = cls
        return cls

class Plugin(metaclass=PluginMeta): ...
class Json(Plugin): ...
class Csv(Plugin): ...

sorted(registry)      # ['Csv', 'Json']
type(Json)            # <class PluginMeta>
type(int)             # <class type>
```

Сопутствующий вопрос — разница `__new__` и `__init__`: `__new__` **создаёт**
объект и возвращает его, `__init__` только настраивает уже созданный. Для
классов ровно то же самое, но на уровне метакласса.

**Подвох.** В подавляющем большинстве случаев метакласс не нужен. Регистрацию
подклассов закрывает `__init_subclass__`, настройку дескрипторов —
`__set_name__`, а изменение класса целиком — декоратор класса. Метаклассы
ещё и конфликтуют при наследовании: у потомка метакласс обязан быть подклассом
всех метаклассов баз, иначе `TypeError`.

```python
class Base:
    def __init_subclass__(cls, /, tag=None, **kwargs):
        super().__init_subclass__(**kwargs)
        print("subclass:", cls.__name__, tag)

class Sub(Base, tag="x"): ...
# subclass: Sub x
```

---

## Что будет, если переопределить `__eq__` и не тронуть `__hash__`?

**Коротко.** Объект станет нехешируемым: Python выставит `__hash__ = None`.
Иначе нарушился бы контракт «равные объекты имеют равный хеш».

```python
class P:
    def __init__(self, x): self.x = x
    def __eq__(self, other):
        return isinstance(other, P) and self.x == other.x

{P(1)}
# TypeError: unhashable type: 'P'
P.__hash__
# None
```

Чинится определением `__hash__` по тем же полям, что и `__eq__`:

```python
class P:
    def __init__(self, x): self.x = x
    def __eq__(self, other): return isinstance(other, P) and self.x == other.x
    def __hash__(self): return hash(self.x)
```

Изменяемые объекты часто оставляют нехешируемыми намеренно — иначе объект,
положенный в `set`, «потеряется» после изменения поля
(см. [Типы данных](data-types.md)). У `@dataclass` то же правило
автоматизировано: `eq=True` (по умолчанию) выключает хеш, а `frozen=True`
его возвращает.

**Глубже.** Соседняя пара — `__repr__` и `__str__`. `__repr__` предназначен
для разработчика и по возможности однозначен (`P(x=1)`), `__str__` — для
пользователя. Если определён только `__repr__`, `str()` использует его;
наоборот — нет. Поэтому в своих классах в первую очередь пишут `__repr__`.

---

[← Пример: bound methods](bound-methods-example.md) · [🏠 Домой](../README.md) · [Управление памятью →](memory-management.md)
