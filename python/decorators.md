# Декораторы

[← bool](bool.md) · [🏠 Домой](../README.md) · [Пример: bound methods →](bound-methods-example.md)

---

Декоратор - достаточно широкое понятие:  
В архитектурном понимании **Декоратор** - это паттерн проектирования, при использовании которого класс или функция изменяет или дополняет функциональность другого класса или функции без использования наследования или прямого изменения исходного кода.  
В понимании сущностей в python **Декоратор** - это функция или вызываемый объект (далее просто функция-декоратор) которая принимает в качестве параметра другую функцию(исходную), и возвращает новую функцию.

```python
TFunc = Callable[..., Any]

def decorator(func: TFunc) -> TFunc:
   pass
```

```python
# ParamSpec из typing доступен начиная с python 3.10 (для более старых версий - typing_extensions)

P = ParamSpec("P")
R = TypeVar("R")

def decorator(f: Callable[P, R]) -> Callable[P, R]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        ...
        res = f(*args, **kwargs)
        ...
        return res
    return inner

```

```python
# python 3.12+: PEP 695 — параметры типа объявляются прямо в сигнатуре функции,
# TypeVar/ParamSpec отдельно импортировать и создавать не нужно
# (подробнее про PEP 695 см. раздел "Тайпинг" ниже)

def decorator[**P, R](f: Callable[P, R]) -> Callable[P, R]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        res = f(*args, **kwargs)
        return res
    return inner
```

Декораторы используются в самых разных случаях.

*Например*:

- кеширование
- валидация
- логирование вызовов функции
- любая другая мидлварь

*Стандартные (built-in) декораторы python:*

- `staticmethod`
- `classmethod`
- `property`

*Декораторы из стандартной библиотеки:*

- from `functools`:
  - `wraps`
  - `lru_cache`
  - `cache` (`python 3.9+`) — упрощённый `lru_cache(maxsize=None)`, без
    ограничения размера
  - `singledispatchmethod`
  - `cached_property`
- from `typing`:
  - `overload`
  - `final`
  - `override` (`python 3.12+`) — см. раздел [Тайпинг](typing-advanced.md)
- from `abc`:
  - `abstractmethod`
  - `abstractclassmethod`
  - `abstractstaticmethod`
  - `abstractproperty`
- from `dataclasses`:
  - `dataclass`
- etc.

```python
# Пример декоратора для логирования вызовов функции
from typing import (
    Callable,
    Optional,
    TypeVar
)
from functools import wraps

R = TypeVar("R")

def call_log_decorator(
        logger: Optional[Callable[[str], ...]] = None, 
        prefix: Optional[str] = None, 
        postfix: Optional[str] = None
) -> Callable[[Callable[..., R]], ...]:
    """
    Декоратор для логирования вызовов функции
    :param logger: Функция для записи логов
    :param prefix: строка префикса для лог-записи
    :param postfix: строка постфикса для лог-записи
    """
    if logger is None:
        logger = print
    if prefix is None:
        prefix = ''
    if postfix is None:
        postfix = ''

    def decorator(func: Callable[..., R]) -> Callable[..., R]:

        @wraps(func)
        def inner(*args, **kwargs) -> R:
            logger(f"{prefix}new call {func!r} with {args = } {kwargs = }{postfix}")
            res = func(*args, **kwargs)
            return res
        return inner
    return decorator


with open('test_log.log', 'a', encoding='utf8') as logfile:
    @call_log_decorator(logfile.write, postfix='\n')

    def foo(a: int, b: bool) -> str:
        return f"{a = }; {b = }"
```

См. также: разобранный пример самодельных `classmethod`/`staticmethod` —
[bound methods своими руками](bound-methods-example.md).

---

[← bool](bool.md) · [🏠 Домой](../README.md) · [Пример: bound methods →](bound-methods-example.md)
