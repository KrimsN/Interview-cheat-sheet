# Пример: bound methods, classmethod и staticmethod своими руками

[← Декораторы](decorators.md) · [🏠 Домой](../README.md) · [ООП вглубь →](oop-advanced.md)

---

## Что такое протокол дескрипторов?

**Коротко.** Дескриптор — объект, который умеет перехватывать доступ к атрибуту
класса. Если у объекта, лежащего в классе, есть `__get__`, то при обращении
`instance.attr` вернётся не он сам, а результат его `__get__`.

Это механизм, на котором в CPython построены `property`, `classmethod`,
`staticmethod` и обычные методы. Различают два вида:

- **non-data дескриптор** — только `__get__`. Приоритет ниже, чем у
  `instance.__dict__`: атрибут экземпляра его перекроет.
- **data дескриптор** — есть `__set__` или `__delete__`. Приоритет **выше**
  `instance.__dict__`, поэтому `property` нельзя случайно затереть присваиванием.

Именно поэтому обычная функция в классе становится методом: функция — это
non-data дескриптор, чей `__get__` возвращает связанный метод (bound method) с
подставленным `self`.

---

## Как это выглядит, если написать руками

Ниже — самодельные аналоги из CPython, с `print` в каждой точке, чтобы увидеть
порядок вызовов.

```python
class MethodType:
    "Аналог PyMethod_Type из Objects/classobject.c"

    def __init__(self, func, obj):
        print(f'MethodType.__init__({func.__name__}, {obj})')
        self.__func__ = func
        self.__self__ = obj

    def __call__(self, *args, **kwargs):
        print(f'MethodType.__call__(args={args})')
        return self.__func__(self.__self__, *args, **kwargs)


class ClassMethod:
    "Аналог PyClassMethod_Type из Objects/funcobject.c"

    def __init__(self, f):
        print(f'ClassMethod.__init__({f.__name__})')
        self.f = f

    def __get__(self, obj, cls=None):
        print(f'ClassMethod.__get__(obj={obj}, cls={cls.__name__})')
        if cls is None:
            cls = type(obj)
        return MethodType(self.f, cls)      # связываем с КЛАССОМ


class StaticMethod:
    "Аналог PyStaticMethod_Type из Objects/funcobject.c"

    def __init__(self, f):
        print(f'StaticMethod.__init__({f.__name__})')
        self.f = f

    def __get__(self, obj, cls=None):
        print('StaticMethod.__get__ -> отдаём функцию как есть')
        return self.f                        # ничего не связываем


class A:
    @ClassMethod
    def from_name(cls, name):
        print(f'  from_name(cls={cls.__name__}, name={name})')

    @StaticMethod
    def helper(x):
        print(f'  helper(x={x})')


print('--- runtime ---')
a = A()
a.from_name('test')
a.helper(42)
```

## Разбор вывода

```
ClassMethod.__init__(from_name)          <- на этапе создания класса
StaticMethod.__init__(helper)
--- runtime ---
ClassMethod.__get__(obj=<A object>, cls=A)   <- доступ к атрибуту
MethodType.__init__(from_name, <class 'A'>)  <- связали с классом, не с a
MethodType.__call__(args=('test',))
  from_name(cls=A, name=test)                <- cls == A, хотя звали через a

StaticMethod.__get__ -> отдаём функцию как есть
  helper(x=42)                               <- никакого первого аргумента
```

Что здесь видно:

1. **Декораторы отработали при создании класса**, а не при вызове — обе строки
   `__init__` напечатались до `--- runtime ---`.
2. **`__get__` вызывается в момент доступа к атрибуту**, каждый раз заново.
   Связанный метод — временный объект, он не хранится в классе.
3. **Разница между `classmethod` и `staticmethod`** — ровно в одной строке
   `__get__`: первый заворачивает функцию в `MethodType`, подставляя класс,
   второй возвращает исходную функцию нетронутой.
4. **`cls` — это `A`, хотя обращались через экземпляр `a`.** Именно поэтому
   `classmethod` годится для альтернативных конструкторов: он получает класс, а
   при вызове от наследника получит наследника.

**Подвох.** Обычный метод устроен так же, только `__get__` подставляет
**экземпляр**: `a.method` создаёт новый bound method при каждом обращении,
поэтому `a.method is a.method` даёт `False`.

---

[← Декораторы](decorators.md) · [🏠 Домой](../README.md) · [ООП вглубь →](oop-advanced.md)
