# Базовый `typing`: `Protocol`, `TypedDict`, `Literal`, `Optional`

## Что нужно знать

В python/ уже разобраны продвинутые темы тайпинга — [PEP 695
generics/`Self`/`override`/отложенные
аннотации](../python/typing-advanced.md),
но нет базового слоя, без которого продвинутые темы плохо понятны:

- **`Optional[X]` vs `X | None`** — `Optional[X]` — эквивалент `Union[X, None]`
  из модуля `typing`; начиная с Python 3.10 (PEP 604) предпочтительнее
  писать `X | None` напрямую (как и `int | str` вместо `Union[int, str]`,
  уже упомянуто в разделе про
  [Union-типы](../python/data-types.md)).
- **`Literal[...]`** — сужает тип до конкретного набора констант
  (`Literal["get", "post"]`), а не любого `str`. Статические анализаторы
  (mypy, pyright) проверяют, что передаётся только одно из перечисленных
  значений, и могут проверять полноту `match`/`if`-веток по `Literal`.
- **`TypedDict`** — описывает словарь с фиксированным набором ключей и
  типов значений (например, структура JSON без создания полноценного
  класса/датакласса). Есть `total=False` для необязательных ключей и
  `Required`/`NotRequired` (3.11+) для точечного управления обязательностью
  отдельных ключей.
- **`Protocol`** — структурная типизация ("утиная типизация" с проверкой
  статическим анализатором): класс считается соответствующим протоколу,
  если у него есть нужные методы/атрибуты, без явного наследования
  (в отличие от ABC, где наследование обязательно). Классический пример —
  `Protocol` с методом `__len__` вместо `Sized` из `collections.abc`, когда
  нужен "любой объект с длиной".
- Важно: всё это — **только для статических анализаторов** (mypy, pyright),
  сам интерпретатор Python аннотации типов в общем случае не проверяет и не
  использует в рантайме (кроме отдельных случаев вроде `dataclasses`,
  которые читают `__annotations__`).

## Ссылки

- [`typing` — официальная документация](https://docs.python.org/3/library/typing.html) — первоисточник по `Protocol`, `TypedDict`, `Literal`, `Optional` и всем остальным конструкциям модуля.
- [PEP 544 – Protocols: Structural subtyping](https://peps.python.org/pep-0544/) — обоснование и механика структурной типизации.
- [PEP 589 – TypedDict](https://peps.python.org/pep-0589/) — первоисточник по `TypedDict`, включая `total=False`.
- [Modern Python Intermediate #2: typing in earnest — Generic, Protocol, TypedDict, Literal — School of Web](https://schoolofweb.net/en/posts/modern-python-intermediate-2-typing-deep/) — связный практический разбор всех четырёх тем вместе.
