# Python — шпаргалка для собеседований

[🏠 Домой](../README.md) · [Типы данных →](data-types.md)

---

Темы в порядке чтения — от основ к продвинутым и версионным фичам.
Каждая тема построена как «вопрос → ответ»: **Коротко** — модель устного
ответа, дальше разбор, рабочий пример с выводом, **Подвох** и **Глубже**.

Черновые темы, которых здесь ещё нет, — в [topics/](../topics/README.md).

1. [Типы данных](data-types.md) — mutable/immutable, передача аргументов, хешируемость
2. [Truthy and Falsy](truthy-falsy.md) — `__bool__` vs `__len__`
3. [int](int.md) — произвольная точность, деление с отрицательными
4. [float](float.md) — IEEE 754, `0.1 + 0.2`, `nan`, округление
5. [str](str.md) — Unicode, PEP 393, f-строки и t-строки
6. [bool](bool.md) — подкласс `int`, что возвращают `and`/`or`
7. [Область видимости: LEGB, замыкания, late binding](scoping-closures.md) — `nonlocal`/`global`, ячейки
8. [Функциональный стиль](functional-programming.md) — `*args`/`**kwargs`, `map`/`filter`/`reduce`, `partial`
9. [Walrus-оператор и позиционно-только параметры](modern-syntax.md) — `python 3.8+`
10. [Декораторы](decorators.md) — `wraps`, порядок, типизация через `ParamSpec`
11. [Пример: bound methods, classmethod, staticmethod своими руками](bound-methods-example.md) — протокол дескрипторов
12. [ООП вглубь](oop-advanced.md) — MRO и `super()`, дескрипторы, `__slots__`, метаклассы, `__eq__`/`__hash__`
13. [Управление памятью](memory-management.md) — refcounting, GC, `weakref`, copy/deepcopy, `is` vs `==`
14. [Итератор](iterators.md) — iterable vs iterator, лень, свой итератор
15. [Генератор](generators.md) — `yield from`, `send`/`throw`/`close`, PEP 479
16. [Comprehensions и генераторные выражения](comprehensions.md) — лень, память, PEP 709
17. [Модуль `itertools`](itertools.md) — `chain`, `islice`, `groupby`, комбинаторика
18. [Модуль `collections`](collections-module.md) — `defaultdict`, `Counter`, `deque`, `namedtuple`
19. [Сортировка](sorting.md) — `sorted()` vs `sort()`, `key`, стабильность, Timsort
20. [Контекстные менеджеры](context-managers.md) — протокол, `contextlib`
21. [match / case (сопоставление с образцом)](pattern-matching.md) — `python 3.10+`
22. [Исключения](exceptions.md) — иерархия, `try/except/else/finally`, `raise ... from ...`
23. [Группы исключений: `except*` и `ExceptionGroup`](exception-groups.md) — `python 3.11+`
24. [GIL и конкурентность](concurrency-gil.md) — threading / multiprocessing / asyncio, корутины и event loop
25. [`asyncio.TaskGroup`](asyncio-taskgroup.md) — `python 3.11+`
26. [Базовый `typing`](typing-basics.md) — `Optional`, `Literal`, `TypedDict`, `Protocol`
27. [Тайпинг: дженерики, `Self`, `override`, отложенные аннотации](typing-advanced.md) — `python 3.11-3.14`
28. [`tomllib`](tomllib.md) — `python 3.11+`
29. [Классы: `dataclasses`, `enum.StrEnum`](classes-dataclasses-enum.md) — `python 3.10-3.11`
30. [CPython без GIL: free-threading, JIT, суб-интерпретаторы](free-threading-jit.md) — `python 3.13+`
31. [Инструменты разработчика: ошибки, REPL, отладка](dev-tools.md) — `python 3.10+`

---

[🏠 Домой](../README.md) · [Типы данных →](data-types.md)
