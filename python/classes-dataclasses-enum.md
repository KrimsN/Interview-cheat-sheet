# Классы: `dataclasses`, `enum.StrEnum`

[← tomllib](tomllib.md) · [🏠 Домой](../README.md) · [CPython без GIL →](free-threading-jit.md)

---

## Что даёт `@dataclass`?

**Коротко.** Автоматически генерирует `__init__`, `__repr__` и `__eq__` по
аннотациям полей — вместо десятка строк шаблонного кода.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int = 0        # значение по умолчанию

Point(1, 2)           # Point(x=1, y=2)  — готовый __repr__
Point(1, 2) == Point(1, 2)   # True — сравнение по значениям, а не по id
```

Полезные параметры:

- `frozen=True` — экземпляры неизменяемы, и класс становится хешируемым.
- `kw_only=True` (`python 3.10+`) — все поля только как именованные аргументы.
- `slots=True` (`python 3.10+`) — автогенерация `__slots__`: экономия памяти и
  запрет случайных новых атрибутов.
- `order=True` — добавляет `__lt__`, `__gt__` и т.д.

```python
# python 3.10+
@dataclass(kw_only=True, slots=True)
class Config:
    host: str
    port: int = 8080

Config(host="localhost")           # ок
Config("localhost")                # TypeError — только по имени
```

**Подвох.** Изменяемое значение по умолчанию **запрещено явно** — Python не даст
повторить классическую ошибку с общим списком:

```python
@dataclass
class Bad:
    items: list = []
# ValueError: mutable default <class 'list'> for field items is not allowed:
#             use default_factory
```

Правильно — через `field(default_factory=...)`, он вызывается на каждый
экземпляр:

```python
from dataclasses import field

@dataclass
class Good:
    items: list = field(default_factory=list)
    total: int = 0

    def __post_init__(self):        # вызывается после __init__
        self.total = len(self.items)

Good(['a', 'b'])          # Good(items=['a', 'b'], total=2)
Good().items is Good().items    # False — списки независимы
```

**Глубже.** `frozen=True` запрещает присваивание через `__setattr__`, выбрасывая
`FrozenInstanceError`. Хешируемость появляется потому, что при `eq=True` Python
обычно убирает `__hash__` (как и при ручном определении `__eq__`), а `frozen`
разрешает его вернуть — неизменяемый объект безопасно класть в `set` и `dict`.

Сравнение с соседями: `namedtuple` легче и неизменяем, но без методов и
значений по умолчанию; `dataclass` гибче; `pydantic` вдобавок **валидирует**
типы в рантайме, чего `dataclass` не делает вовсе.

---

## Чем `StrEnum` отличается от обычного `Enum`?

**Коротко.** `python 3.11+`. Члены `StrEnum` одновременно являются строками,
поэтому их можно сравнивать и сериализовать напрямую, без `.value`.

```python
# python 3.11+
from enum import StrEnum, auto

class Colour(StrEnum):
    RED = "red"
    GREEN = auto()      # auto() даёт имя в нижнем регистре -> 'green'

Colour.RED == "red"     # True
f"{Colour.RED}"         # 'red'
```

Обычный `Enum` так не умеет — и это осознанно:

```python
from enum import Enum

class Plain(Enum):
    A = "a"

Plain.A == "a"      # False — нужен Plain.A.value
```

Аналогично `IntEnum` ведёт себя как целое: `Priority.HIGH > 1` работает.

**Подвох.** У «смешанных» enum (`StrEnum`, `IntEnum`) есть цена: они неявно
приводятся к базовому типу, поэтому теряется часть защиты от ошибок — функция,
ожидающая строку, молча примет член enum и наоборот. Обычный `Enum` строже:
такое сравнение вернёт `False`, и ошибка вылезет сразу.

**Глубже.** `auto()` в `StrEnum` даёт имя члена в нижнем регистре — это отличие
от обычного `Enum`, где `auto()` выдаёт числа `1, 2, 3...`.

---

[← tomllib](tomllib.md) · [🏠 Домой](../README.md) · [CPython без GIL →](free-threading-jit.md)
