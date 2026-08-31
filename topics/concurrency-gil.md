# GIL и конкурентность: threading / multiprocessing / asyncio

## Что нужно знать

- **GIL (Global Interpreter Lock)** — мьютекс в CPython, разрешающий
  выполнять байткод Python только одному потоку одновременно. Существует
  в первую очередь из-за того, что управление памятью в CPython построено
  на подсчёте ссылок (reference counting) — без GIL несколько потоков могли
  бы одновременно менять счётчик ссылок и повредить память. Про
  free-threading сборку (PEP 703, 3.13+/3.14+) уже есть раздел в
  [python/free-threading-jit.md](../python/free-threading-jit.md)
  — эту тему стоит увязать именно с объяснением GIL.
- **I/O-bound vs CPU-bound** — ключевой критерий выбора инструмента:
  - **I/O-bound без async-библиотек** (блокирующие сетевые/файловые
    вызовы) → `threading`. GIL освобождается на время I/O-операции, поэтому
    потоки реально помогают.
  - **I/O-bound с высокой конкурентностью** (сотни-тысячи одновременных
    запросов) → `asyncio`. Работает в одном потоке, переключение между
    задачами — только в точках `await`, оверхед на задачу минимален.
  - **CPU-bound** (математика, обработка изображений) → `multiprocessing`.
    Каждый процесс — свой интерпретатор и свой GIL, поэтому это единственный
    вариант получить реальный параллелизм на нескольких ядрах в GIL-сборке.
    Минусы: дорогое создание процессов, обмен данными требует сериализации
    (pickle).
  - Использовать `threading` для CPU-bound задач — классическая ошибка:
    из-за GIL параллельного выполнения байткода не будет, а из-за
    переключения контекста может быть даже медленнее одного потока.
- **`concurrent.futures`** — `ThreadPoolExecutor`/`ProcessPoolExecutor` как
  унифицированный высокоуровневый интерфейс поверх threading/multiprocessing.
- **Основы asyncio** — `async def`/`await`, корутины, event loop,
  `asyncio.run()`. В python/ уже есть продвинутая тема
  [`asyncio.TaskGroup`](../python/asyncio-taskgroup.md) — но нет базы про то,
  что такое корутина и как работает цикл событий, стоит добавить перед ней.

## Ссылки

- [Global Interpreter Lock — Python Glossary](https://docs.python.org/3/glossary.html#term-global-interpreter-lock) — официальное определение GIL.
- [`threading` — официальная документация](https://docs.python.org/3/library/threading.html) и [`multiprocessing` — официальная документация](https://docs.python.org/3/library/multiprocessing.html) — первоисточники по API.
- [`asyncio` — официальная документация](https://docs.python.org/3/library/asyncio.html) — стартовая точка по корутинам и event loop.
- [asyncio vs threading vs multiprocessing: When to Use Each in Python — BSWEN](https://docs.bswen.com/blog/2026-04-14-asyncio-vs-threading-vs-multiprocessing/) — сравнение трёх подходов с акцентом на "когда что выбирать".
- [Python Concurrency for Data Engineers — DriveDataScience](https://www.drivedatascience.com/python-concurrency-threading-multiprocessing-asyncio-threadpool-processpool-gil/) — развёрнутый разбор всех паттернов конкурентности с примерами кода.
