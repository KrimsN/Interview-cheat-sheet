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
7. [Декораторы](decorators.md) — `wraps`, порядок, типизация через `ParamSpec`
8. [Пример: bound methods, classmethod, staticmethod своими руками](bound-methods-example.md) — протокол дескрипторов
9. [Итератор](iterators.md) — iterable vs iterator, лень, свой итератор
10. [Генератор](generators.md) — `yield from`, `send`/`throw`/`close`, PEP 479
11. [match / case (сопоставление с образцом)](pattern-matching.md) — `python 3.10+`
12. [Группы исключений: `except*` и `ExceptionGroup`](exception-groups.md) — `python 3.11+`
13. [`asyncio.TaskGroup`](asyncio-taskgroup.md) — `python 3.11+`
14. [Тайпинг: дженерики, `Self`, `override`, отложенные аннотации](typing-advanced.md) — `python 3.11-3.14`
15. [`tomllib`](tomllib.md) — `python 3.11+`
16. [Классы: `dataclasses`, `enum.StrEnum`](classes-dataclasses-enum.md) — `python 3.10-3.11`
17. [CPython без GIL: free-threading, JIT, суб-интерпретаторы](free-threading-jit.md) — `python 3.13+`
18. [Инструменты разработчика: ошибки, REPL, отладка](dev-tools.md) — `python 3.10+`

---

[🏠 Домой](../README.md) · [Типы данных →](data-types.md)
