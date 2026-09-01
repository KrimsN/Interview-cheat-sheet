# Декораторы

[← Walrus-оператор](modern-syntax.md) · [🏠 Домой](../README.md) · [Пример: bound methods →](bound-methods-example.md)

---

## Что такое декоратор?

**Коротко.** Функция (или любой вызываемый объект), которая принимает функцию и
возвращает новую функцию, добавляя поведение вокруг исходной. Синтаксис `@dec`
над `def f` — это просто сахар для `f = dec(f)`.

Начнём с самого простого рабочего декоратора — он печатает вызов и результат:

```python
from functools import wraps

def log(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print(f"-> {func.__name__}{args}")
        res = func(*args, **kwargs)
        print(f"<- {res}")
        return res
    return inner

@log
def add(a, b):
    return a + b

add(2, 3)
# -> add(2, 3)
# <- 5
```

В архитектурном смысле это паттерн «Декоратор»: поведение добавляется без
наследования и без правки исходного кода.

**Подвох.** «Когда выполняется тело декоратора?» В момент определения функции,
один раз — а не при каждом вызове. При каждом вызове выполняется только `inner`.

---

## Зачем нужен `functools.wraps`?

**Коротко.** Без него декорированная функция теряет своё имя, docstring и
сигнатуру — снаружи виден `inner`, а не исходная функция.

```python
def bare(func):
    def inner(*a, **k): return func(*a, **k)
    return inner

@bare
def foo():
    "док foo"

foo.__name__   # 'inner'   — имя потеряно
foo.__doc__    # None      — docstring потерян
```

С `@wraps(func)` метаданные копируются, а в `__wrapped__` кладётся ссылка на
оригинал — по ней работает интроспекция (`inspect.signature`, отладчики,
документация).

**Подвох.** Это частый вопрос «что сломается, если не написать `wraps`». Ломается
не выполнение, а всё, что смотрит на функцию снаружи: трейсбеки становятся
нечитаемыми, `help()` пустеет, инструменты вроде Sphinx и pytest начинают
путаться.

---

## В каком порядке применяются несколько декораторов?

**Коротко.** Снизу вверх при применении, сверху вниз при вызове. Ближайший к
`def` оборачивает первым.

```python
@A
@B
def target(): ...

# эквивалентно target = A(B(target))
```

При вызове первым отработает внешний `A`, затем `B`, затем сама функция.

---

## Как написать декоратор с аргументами?

**Коротко.** Нужен ещё один уровень вложенности: внешняя функция принимает
аргументы и возвращает собственно декоратор.

```python
from functools import wraps

def call_log_decorator(logger=None, prefix="", postfix=""):
    """Декоратор для логирования вызовов функции.

    :param logger: функция, принимающая строку (print, list.append, log.info)
    :param prefix: префикс лог-записи
    :param postfix: постфикс лог-записи
    """
    if logger is None:
        logger = print

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            logger(f"{prefix}call {func.__name__} {args=} {kwargs=}{postfix}")
            return func(*args, **kwargs)
        return inner
    return decorator


lines = []

@call_log_decorator(lines.append)
def calc(a, b=1):
    return a * b

calc(6, b=7)
# lines -> ["call calc args=(6,) kwargs={'b': 7}"]
```

**Подвох.** Логгером тут стоит передавать функцию, а не связанный метод живого
ресурса. Если написать `@call_log_decorator(logfile.write)` внутри блока
`with open(...) as logfile`, декоратор захватит `logfile.write` в замыкание, а
к моменту вызова функции файл будет уже закрыт — получите
`ValueError: I/O operation on closed file`. Открывать файл нужно на всё время
жизни декорированной функции либо логировать через `logging`.

---

## Как задекорировать так, чтобы не сломать типизацию?

**Коротко.** Через `ParamSpec` + `TypeVar` — они сохраняют сигнатуру исходной
функции, в отличие от `Callable[..., Any]`.

```python
# ParamSpec доступен с python 3.10 (раньше — из typing_extensions)
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def decorator(f: Callable[P, R]) -> Callable[P, R]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        return f(*args, **kwargs)
    return inner
```

`python 3.12+` (PEP 695) — параметры типа объявляются прямо в сигнатуре,
`TypeVar`/`ParamSpec` создавать вручную больше не нужно:

```python
# python 3.12+
def decorator[**P, R](f: Callable[P, R]) -> Callable[P, R]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        return f(*args, **kwargs)
    return inner
```

Подробнее про PEP 695 — в разделе [Тайпинг](typing-advanced.md).

**Подвох.** `...` в `Callable` допустим **только** на месте списка аргументов
(`Callable[..., R]` — «любые аргументы»), но не на месте возвращаемого типа.
`Callable[[str], ...]` — ошибка, mypy отвечает `Unexpected "..."`. Правильно —
`Callable[[str], None]`.

---

## Декоратор обязательно функция?

Нет — подойдёт любой вызываемый объект. Класс удобен, когда декоратору нужно
хранить состояние:

```python
from functools import wraps

class CountCalls:
    def __init__(self, func):
        wraps(func)(self)
        self.func = func
        self.n = 0

    def __call__(self, *args, **kwargs):
        self.n += 1
        return self.func(*args, **kwargs)

@CountCalls
def ping(): ...

ping(); ping()
ping.n   # 2
```

---

## Какие декораторы есть в стандартной библиотеке?

*Встроенные:*

- `staticmethod`, `classmethod`, `property`

*Из `functools`:*

- `wraps` — сохранить метаданные обёрнутой функции
- `lru_cache` — кеш с ограничением размера
- `cache` (`python 3.9+`) — то же, что `lru_cache(maxsize=None)`
- `cached_property` — свойство, вычисляемое один раз на экземпляр
- `singledispatch` / `singledispatchmethod` — диспетчеризация по типу аргумента

*Из `typing`:*

- `overload`, `final`
- `override` (`python 3.12+`) — см. [Тайпинг](typing-advanced.md)

*Из `abc`:*

- `abstractmethod`

*Из `dataclasses`:*

- `dataclass`

**Подвох.** `abstractclassmethod`, `abstractstaticmethod` и `abstractproperty`
**устарели с python 3.3**. Современная идиома — комбинировать обычный декоратор
с `abstractmethod`, причём `abstractmethod` должен быть ближе к `def`:

```python
from abc import ABC, abstractmethod

class Base(ABC):
    @classmethod
    @abstractmethod
    def create(cls): ...
```

**Глубже.** `lru_cache` на методе держит сильную ссылку на `self` через ключ
кеша — экземпляры перестают собираться сборщиком мусора, и получается утечка
памяти. Для методов используют `cached_property` или кеш на уровне экземпляра.

---

См. также разобранный пример того, как `classmethod`/`staticmethod` устроены
изнутри — [bound methods своими руками](bound-methods-example.md).

---

[← Walrus-оператор](modern-syntax.md) · [🏠 Домой](../README.md) · [Пример: bound methods →](bound-methods-example.md)
