# Тайпинг: дженерики, `Self`, `override`, отложенные аннотации

[← asyncio.TaskGroup](asyncio-taskgroup.md) · [🏠 Домой](../README.md) · [tomllib →](tomllib.md)

---

**`typing.Self`** (`python 3.11+`) — удобная аннотация для методов,
возвращающих экземпляр своего же класса (альтернативные конструкторы,
fluent-интерфейсы, контекстные менеджеры):

```python
# python 3.11+
from typing import Self

class Builder:
    def add(self, item) -> Self:
        ...
        return self
```

**PEP 695: новый синтаксис дженериков и `type`-алиасы** (`python 3.12+`) —
больше не обязательно вручную создавать `TypeVar`/`ParamSpec`/`TypeVarTuple`,
параметры типа объявляются прямо в сигнатуре класса/функции (пример с
декоратором см. [в разделе Декораторы](decorators.md)):

```python
# python 3.12+
class Stack[T]:
    def push(self, item: T) -> None: ...
    def pop(self) -> T: ...

type IntOrStrSequence[T: (int, str)] = list[T]
```

**`typing.override`** (`python 3.12+`) — явно помечает переопределение
метода родителя: статические анализаторы (mypy, pyright) подсветят ошибку,
если в родительском классе такого метода нет (например, из-за опечатки):

```python
# python 3.12+
from typing import override

class Base:
    def get_color(self) -> str: ...

class Child(Base):
    @override
    def get_color(self) -> str:
        return "yellow"
```

**Отложенное вычисление аннотаций по умолчанию** (`python 3.14+`, PEP
649 / PEP 749) — аннотации типов (`def f(x: SomeType)`, переменные класса и
т.д.) больше не вычисляются при определении функции/класса, а лежат
"лениво" и вычисляются по требованию через модуль `annotationlib`. Раньше
для этого нужен был `from __future__ import annotations` (PEP 563) — теперь
это поведение по умолчанию, и forward-ссылки на ещё не объявленные типы
работают без строковых аннотаций:

```python
# < python 3.14: без from __future__ import annotations была бы NameError
class Node:
    next: "Node | None" = None

# python 3.14+: кавычки больше не обязательны для forward-ссылок
class Node:
    next: Node | None = None
```

---

[← asyncio.TaskGroup](asyncio-taskgroup.md) · [🏠 Домой](../README.md) · [tomllib →](tomllib.md)
