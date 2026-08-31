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

## Проверяет ли Python аннотации типов во время выполнения?

**Коротко.** Нет. Аннотации — это информация для статических анализаторов
(mypy, pyright) и для интроспекции. Интерпретатор их не проверяет и на их
основании ничего не решает.

```python
def f(x: int) -> str:
    return x        # mypy ругается, но код прекрасно выполняется

f("не число")       # никакой ошибки в рантайме
```

Это, пожалуй, самый частый вопрос по теме — и он же объясняет, зачем вообще
нужен отдельный шаг проверки типов в CI.

**Подвох.** Исключения есть, и они важны: аннотации **читают** библиотеки.
`dataclasses` по ним генерирует `__init__`, `pydantic` — валидирует значения,
FastAPI — разбирает и приводит параметры запроса. Но делает это библиотека,
читая `__annotations__`, а не сам интерпретатор.

**Глубже.** Из-за отложенного вычисления аннотаций (`python 3.14+`, PEP 649)
доставать их напрямую из `__annotations__` стало ненадёжно — правильный способ
теперь `annotationlib.get_annotations()` или `typing.get_type_hints()`, которые
корректно разрешают forward-ссылки.

---

[← asyncio.TaskGroup](asyncio-taskgroup.md) · [🏠 Домой](../README.md) · [tomllib →](tomllib.md)
