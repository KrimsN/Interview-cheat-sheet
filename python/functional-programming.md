# Функциональный стиль: `*args`/`**kwargs`, `map`/`filter`/`reduce`, `partial`

[← Область видимости](scoping-closures.md) · [🏠 Домой](../README.md) · [Walrus-оператор →](modern-syntax.md)

---

## Что означают `*args` и `**kwargs`?

**Коротко.** В определении функции `*args` собирает лишние позиционные
аргументы в кортеж, `**kwargs` — лишние именованные в словарь. В вызове те же
звёздочки работают наоборот — распаковывают последовательность и словарь
в аргументы.

```python
def f(a, b=2, *args, key=None, **kwargs):
    print(a, b, args, key, kwargs)

f(1, 2, 3, 4, key="k", extra=5)
# 1 2 (3, 4) k {'extra': 5}

args = (1, 2)
kw = {"key": "z"}
f(*args, **kw)
# 1 2 () z {}
```

Важное следствие: всё, что идёт **после** `*args` (или после голой `*`), может
быть передано только по имени — это keyword-only параметры. Так делают опции,
которые не должны читаться как «третий позиционный аргумент».

```python
def connect(host, *, timeout=5, retries=3): ...

connect("db", 10)          # TypeError: takes 1 positional argument but 2 were given
connect("db", timeout=10)  # ok
```

**Подвох.** Имена `args`/`kwargs` — только соглашение; значение имеют
звёздочки. И `*args` — кортеж, а не список: он неизменяем.

**Глубже.** Зеркальный механизм — позиционно-только параметры через `/`
(`def f(a, b, /, c)`): такие имена нельзя передать по ключу, что позволяет
переименовывать их без слома обратной совместимости. Так объявлено большинство
функций из C-модулей стандартной библиотеки.

---

## Чем `map`/`filter` отличаются от comprehension?

**Коротко.** Результат тот же, но `map`/`filter` возвращают ленивые итераторы
и требуют готовой функции, а comprehension читается как выражение и позволяет
писать произвольное преобразование прямо на месте. В Python идиоматичен
comprehension — кроме случая, когда функция уже есть.

```python
list(map(str.upper, ["a", "b"]))   # ['A', 'B']
[s.upper() for s in ["a", "b"]]    # ['A', 'B'] — то же самое

# map выигрывает, когда преобразование — готовая функция
list(map(int, ["1", "2"]))
# лямбда вместо готовой функции — признак, что нужен comprehension
list(map(lambda s: s.strip().lower(), data))   # так лучше не писать
```

`filter(None, iterable)` — идиома «оставить только truthy-значения»
(см. [Truthy and Falsy](truthy-falsy.md)):

```python
list(filter(None, [0, 1, "", "x", []]))
# [1, 'x']
```

**Подвох.** `map` и `filter` в Python 3 — итераторы, а не списки: их можно
пройти один раз, а `len()` от них не берётся. Отсюда классическая ошибка —
дважды пройтись по результату `map` и получить пустоту на втором проходе.

---

## Что делает `functools.reduce` и почему его редко используют?

**Коротко.** `reduce` сворачивает последовательность в одно значение, применяя
функцию по накоплению. В Python 3 он вынесен из builtins в `functools` — как
менее читаемый, чем явный цикл или специализированные `sum`/`math.prod`/`any`.

```python
from functools import reduce

reduce(lambda a, b: a * b, [1, 2, 3, 4])      # 24
reduce(lambda a, b: a + b, [], 0)             # 0 — initial спасает от ошибки
```

**Подвох.** Без начального значения `reduce` на пустой последовательности
бросает `TypeError: reduce() of empty iterable with no initial value`. Третий
аргумент — не «ещё один элемент», а страховка от пустого входа.

**Глубже.** Гвидо ван Россум предлагал выкинуть `reduce` вместе с `lambda`
ещё в «The fate of reduce() in Python 3000». В итоге его сослали в `functools`,
а типовые свёртки закрыли встроенными функциями: `sum`, `min`/`max`, `any`/`all`,
`math.prod`, `itertools.accumulate` (когда нужны промежуточные результаты).

---

## Зачем нужен `functools.partial`?

**Коротко.** Он фиксирует часть аргументов и возвращает новый вызываемый
объект. Это то же, что лямбда-обёртка, но без захвата переменных — значения
запоминаются в момент создания, а не в момент вызова.

```python
from functools import partial

def log(msg, *, level="INFO"):
    return f"{level}: {msg}"

warn = partial(log, level="WARN")
warn("disk")
# 'WARN: disk'
```

Именно поэтому `partial` — штатный обход late binding в циклах: `partial(f, i)`
кладёт текущее `i` внутрь объекта, тогда как `lambda: f(i)` сошлётся на
переменную (см. [Область видимости](scoping-closures.md)).

**Глубже.** `partial` — объект, а не функция: у него есть атрибуты `func`,
`args`, `keywords`. Начиная с Python 3.14 `partial` — дескриптор метода (есть
`__get__`), поэтому при обращении через экземпляр класса он превращается
в bound method, а не остаётся голым `partial`-объектом:

```python
from functools import partial

def f(a, b): return (a, b)

class C:
    m = partial(f, "FIXED")

C().m  # bound method, не просто partial-объект (начиная с 3.14)
```

В Python 3.13 это поведение ещё переходное — обращение к такому атрибуту
через класс/экземпляр выдаёт `FutureWarning: functools.partial will be
a method descriptor in future Python versions`. Чтобы сохранить старое
поведение (не-метод, как раньше), достаточно обернуть в `staticmethod`:
`m = staticmethod(partial(f, "FIXED"))`. Для «метода с заранее фиксированным
аргументом» по-прежнему есть специализированный `functools.partialmethod`.

---

[← Область видимости](scoping-closures.md) · [🏠 Домой](../README.md) · [Walrus-оператор →](modern-syntax.md)
