# Классы: `dataclasses`, `enum.StrEnum`

[← tomllib](tomllib.md) · [🏠 Домой](../README.md) · [CPython без GIL →](free-threading-jit.md)

---

- `dataclasses.dataclass(kw_only=True)` (`python 3.10+`) — заставляет поля
  датакласса принимать значения только как keyword-аргументы.
- `dataclasses.dataclass(slots=True)` (`python 3.10+`) — автогенерация
  `__slots__` для инстансов датакласса (экономия памяти, запрет случайных
  новых атрибутов).
- `enum.StrEnum` (`python 3.11+`) — enum, значения которого одновременно
  являются `str` (не нужно City.MOSCOW.value, можно сравнивать/сериализовать
  сам член enum как строку).

```python
# python 3.10+
from dataclasses import dataclass

@dataclass(kw_only=True, slots=True)
class Point:
    x: int
    y: int
```

```python
# python 3.11+
from enum import StrEnum

class Color(StrEnum):
    RED = "red"
    GREEN = "green"
```

---

[← tomllib](tomllib.md) · [🏠 Домой](../README.md) · [CPython без GIL →](free-threading-jit.md)
