# Контекстные менеджеры: протокол, `contextlib`

## Что нужно знать

- **Протокол** — любой объект с методами `__enter__(self)` и
  `__exit__(self, exc_type, exc_value, traceback)` может использоваться в
  `with`. `__enter__` возвращает значение, которое попадёт в `as` переменную.
  `__exit__` возвращает `True`/truthy, чтобы **подавить** возникшее
  исключение (это частый вопрос-ловушка: если `__exit__` явно не вернул
  `True`, исключение продолжит распространяться после блока `with`).
- **Зачем нужен `with` вместо `try/finally`** — гарантирует освобождение
  ресурса (файл, соединение, лок) даже при исключении, но компактнее и
  явно указывает на "область жизни" ресурса.
- **`contextlib.contextmanager`** — превращает функцию-генератор в
  контекстный менеджер без написания класса: код до `yield` — это
  `__enter__`, код после (обычно в `finally`) — `__exit__`, значение из
  `yield` — то, что попадёт в `as`.
- **Полезные утилиты `contextlib`**:
  - `suppress(*exceptions)` — заменяет `try/except: pass` для игнорирования
    конкретных исключений.
  - `ExitStack` — динамическое управление произвольным числом контекстных
    менеджеров (когда их количество не известно заранее).
  - `closing(obj)` — оборачивает объект с методом `.close()` в контекстный
    менеджер, если тот сам не поддерживает протокол.
- **Несколько менеджеров в одном `with`** — `with open(a) as f1, open(b) as f2:`
  эквивалентно вложенным `with`, порядок выхода — обратный порядку входа.

## Ссылки

- [`contextlib` — официальная документация](https://docs.python.org/3/library/contextlib.html) — первоисточник по `contextmanager`, `suppress`, `ExitStack` и т.д.
- [Python's `with` Statement: Manage External Resources Safely — Real Python](https://realpython.com/python-with-statement/) — подробный разбор протокола `__enter__`/`__exit__` и типовых сценариев.
- [Comprehensive Tutorial on Writing Custom Context Managers in Python — DataCamp](https://www.datacamp.com/tutorial/writing-custom-context-managers-in-python) — сравнение class-based и function-based (декоратор) подходов с примерами.
