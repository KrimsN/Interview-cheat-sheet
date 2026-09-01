# Базовый `typing`: `Optional`, `Literal`, `TypedDict`, `Protocol`

[← asyncio.TaskGroup](asyncio-taskgroup.md) · [🏠 Домой](../README.md) · [Тайпинг: дженерики →](typing-advanced.md)

---

## Проверяет ли Python аннотации типов?

**Коротко.** Нет. Аннотации — это метаданные для статических анализаторов
(mypy, pyright, ty) и для библиотек, читающих их в рантайме. Сам интерпретатор
их не проверяет.

```python
def f(x: int) -> str: ...
f("вообще-то строка")     # никакой ошибки — программа работает

from dataclasses import dataclass

@dataclass
class D:
    x: int

D("строка")
# D(x='строка')  — dataclass использует аннотации, но типы не проверяет
```

Аннотации доступны через `__annotations__` и, аккуратнее, через
`typing.get_type_hints()` — он разрешает строковые (отложенные) аннотации:

```python
from typing import get_type_hints
get_type_hints(f)
# {'x': <class 'int'>, 'return': <class 'str'>}
```

**Подвох.** «Раз не проверяет — можно писать что угодно» неверно ровно
наоборот: неверная аннотация хуже её отсутствия, потому что читатель и
анализатор ей верят. Валидацию в рантайме дают отдельные библиотеки
(pydantic, attrs), и они как раз строят её поверх аннотаций.

---

## `Optional[X]` или `X | None`?

**Коротко.** Это одно и то же (`Optional[X]` — синоним `Union[X, None]`), но
с Python 3.10 (PEP 604) пишут `X | None`: короче, не требует импорта и
единообразно с `int | str` вместо `Union[int, str]`.

```python
Optional[int] == Union[int, None]     # True

def find(uid: int) -> User | None: ...   # современная форма
```

**Подвох.** `Optional` означает «может быть `None`», а **не** «параметр
необязателен». Необязательность задаётся значением по умолчанию, и это
независимые вещи:

```python
def f(a: int | None, b: int = 0): ...
# a — обязателен, но может быть None
# b — необязателен, но None ему передать нельзя
```

**Глубже.** Реже нужные, но узнаваемые: `Any` отключает проверку (анализатор
пропускает всё), `object` — наоборот, требует явного сужения перед
использованием; `Never`/`NoReturn` — для функций, которые не возвращают
управления. Полезная привычка — включить в анализаторе запрет неявного
`Any`, иначе типизация тихо вырождается.

---

## Что даёт `Literal`?

**Коротко.** Сужает тип до конкретного набора значений-констант: не «какая-то
строка», а ровно `"r"` или `"w"`.

```python
from typing import Literal

def open_file(path: str, mode: Literal["r", "w", "a"] = "r") -> None: ...

open_file("f.txt", "x")
# в рантайме ничего; mypy: Argument 2 has incompatible type "Literal['x']"
```

Второе применение — **исчерпывающая** проверка ветвлений: анализатор знает
полный набор значений и укажет на забытую ветку `match`/`if`, что особенно
полезно с [match / case](pattern-matching.md).

**Глубже.** Когда набор значений живёт и в рантайме (валидация, сериализация,
БД), правильнее взять `enum.StrEnum`
(см. [Классы](classes-dataclasses-enum.md)): `Literal` существует только
для анализатора, а enum — настоящий объект. Соседняя конструкция —
`LiteralString` (PEP 675) для защиты от SQL-инъекций: он требует, чтобы строка
была собрана из литералов, а не из пользовательского ввода.

---

## Зачем `TypedDict`, если есть `dataclass`?

**Коротко.** `TypedDict` описывает **обычный словарь** с известным набором
ключей — это способ типизировать JSON и данные, которые всё равно приходят
и уходят словарями, не превращая их в объекты.

```python
from typing import TypedDict, NotRequired

class User(TypedDict):
    id: int
    name: str
    email: NotRequired[str]      # python 3.11+

u: User = {"id": 1, "name": "a"}
type(u)                          # <class 'dict'> — это по-прежнему словарь
```

- `total=False` в объявлении делает необязательными **все** ключи;
- `Required[...]` / `NotRequired[...]` (Python 3.11+) управляют
  обязательностью каждого ключа по отдельности;
- интроспекция: `User.__required_keys__`, `User.__optional_keys__`.

**Подвох.** Никакой проверки в рантайме нет — это буквально `dict`. Строка
`bad: User = {"id": "not-int"}` выполнится молча, ошибку покажет только
анализатор. Если нужна валидация входящего JSON — это pydantic, а не
`TypedDict`.

Выбор простой: данные приходят и остаются словарями → `TypedDict`; нужны
поведение, методы, `__post_init__`, неизменяемость → `dataclass`.

---

## Чем `Protocol` отличается от абстрактного класса?

**Коротко.** `Protocol` (PEP 544) — структурная типизация: класс подходит,
если у него есть нужные методы, без всякого наследования. ABC — номинальная:
нужно явно унаследоваться и зарегистрироваться.

```python
from typing import Protocol

class Closeable(Protocol):
    def close(self) -> None: ...

def shutdown(resource: Closeable) -> None:
    resource.close()
```

Подойдёт любой объект с методом `close()` — файл, сокет, соединение с БД, —
и его автору не нужно знать о существовании `Closeable`. Это и есть «утиная
типизация, которую видит анализатор».

**Подвох.** `isinstance()` с протоколом по умолчанию запрещён — нужен
декоратор `@runtime_checkable`, и даже тогда проверяется **только наличие
методов**, не их сигнатуры:

```python
from typing import runtime_checkable

@runtime_checkable
class Sized(Protocol):
    def __len__(self) -> int: ...

class Box:
    def __len__(self): return 3

isinstance(Box(), Sized)   # True
isinstance(5, Sized)       # False
```

**Глубже.** Для типовых протоколов ничего писать не нужно — готовые лежат в
`collections.abc`: `Iterable`, `Iterator`, `Sized`, `Callable`, `Mapping`,
`Sequence`. Их и берут в аннотациях аргументов: принимать `Iterable[str]`
вместо `list[str]` — правило «принимай максимально общее, возвращай
максимально конкретное».

Дальше — дженерики нового синтаксиса, `Self` и `override`:
[Тайпинг: дженерики, `Self`, `override`, отложенные аннотации](typing-advanced.md).

---

[← asyncio.TaskGroup](asyncio-taskgroup.md) · [🏠 Домой](../README.md) · [Тайпинг: дженерики →](typing-advanced.md)
