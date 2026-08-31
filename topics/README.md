# Темы для собеседования по Python — что доучить

Список тем, которые слабо или совсем не покрыты в [python/](../python/index.md)
(там сейчас в основном базовые типы данных и версионные фичи 3.10-3.14), но
регулярно всплывают на технических собеседованиях. По каждой теме — краткое
резюме и подборка рекомендуемых ссылок (официальная документация в
приоритете, дальше — проверенные разборы).

Это черновой материал для последующего наполнения `python/`, а не готовые
шпаргалки — ссылки нужно будет прочитать и переписать выжимку своими
словами в основном разделе.

## Список тем

- [ООП вглубь: MRO, дескрипторы, метаклассы, `__slots__`](oop-advanced.md)
- [GIL и конкурентность: threading / multiprocessing / asyncio](concurrency-gil.md)
- [Управление памятью: refcounting, GC, weakref, copy/deepcopy](memory-management.md)
- [Область видимости: LEGB, замыкания, `nonlocal`/`global`, late binding](scoping-closures.md)
- [Функциональный стиль: `*args`/`**kwargs`, `map`/`filter`/`reduce`, `functools.partial`](functional-programming.md)
- [Модуль `collections`: `defaultdict`, `Counter`, `deque`, `namedtuple`](collections-module.md)
- [Исключения: иерархия, `try/except/else/finally`, `raise ... from ...`](exceptions.md)
- [Контекстные менеджеры: протокол, `contextlib`](context-managers.md)
- [Comprehensions vs генераторные выражения](comprehensions.md)
- [Сортировка: `sorted()`, `key`, Timsort](sorting.md)
- [Модуль `itertools`](itertools.md)
- [Базовый `typing`: `Protocol`, `TypedDict`, `Literal`, `Optional`](typing-basics.md)
- [Синтаксис 3.8: walrus-оператор, позиционно-только параметры](modern-syntax.md)
