# Исключения: иерархия, `try/except/else/finally`, `raise ... from ...`

## Что нужно знать

- **Иерархия исключений** — все встроенные исключения наследуются от
  `BaseException`, при этом `Exception` — отдельная ветка, от которой
  наследуются "обычные" ошибки (`SystemExit`, `KeyboardInterrupt`,
  `GeneratorExit` умышленно наследуются напрямую от `BaseException`, чтобы
  `except Exception` их не перехватывал). Собеседуют часто именно на этом
  — "почему `except Exception` не ловит `KeyboardInterrupt`".
- **`try/except/else/finally`** — `else` выполняется, только если исключения
  не было (лучше, чем добавлять код в конец `try`, чтобы случайно не
  поймать в `except` исключение из "уже успешного" кода); `finally`
  выполняется всегда, в том числе при `return`/`break` внутри `try` —
  типовое место для закрытия ресурсов.
- **Порядок и специфичность `except`** — сначала более специфичные
  исключения, затем более общие (иначе более общий блок "перехватит" всё,
  а специфичный станет недостижим). Голый `except:` (без указания типа)
  — антипаттерн, ловит вообще всё, включая `SystemExit`/`KeyboardInterrupt`.
- **`raise ... from ...`** — явное связывание исключений
  (exception chaining), сохраняет исходную причину в `__cause__` и в
  трейсбеке ("The above exception was the direct cause..."). `raise ... from None`
  — явно подавляет цепочку, если исходное исключение неинформативно.
- **Кастомные исключения** — наследование от `Exception` (или более
  специфичного встроенного класса), собственная иерархия для доменных
  ошибок приложения. Хорошая практика — не наследоваться напрямую от
  `BaseException`.
- Связь с продвинутой темой в python.md — [`except*` и
  `ExceptionGroup`](../python.md#группы-исключений-except-и-exceptiongroup)
  (3.11+) — это следующий уровень после базового `try/except`, для
  конкурентного кода, где может "упасть" сразу несколько задач.

## Ссылки

- [Errors and Exceptions — официальный туториал Python](https://docs.python.org/3/tutorial/errors.html) — база: `try/except/else/finally`, `raise from`, иерархия исключений.
- [Built-in Exceptions — официальная документация](https://docs.python.org/3/library/exceptions.html) — полное дерево наследования встроенных исключений.
- [Python Exceptions: An Introduction — Real Python](https://realpython.com/python-exceptions/) — практический разбор с акцентом на best practices и кастомные исключения.
