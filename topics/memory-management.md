# Управление памятью: refcounting, GC, weakref, copy/deepcopy

## Что нужно знать

- **Подсчёт ссылок (reference counting)** — у каждого объекта в CPython есть
  счётчик ссылок. Как только он падает до нуля, память объекта освобождается
  немедленно (в отличие от, например, Java с "чистым" трассирующим GC).
  `sys.getrefcount(obj)` показывает текущее значение.
- **Циклический сборщик мусора (`gc`)** — reference counting не умеет
  находить циклические ссылки (`a.x = b; b.x = a`), поэтому отдельно
  работает generational garbage collector (поколения 0/1/2, алгоритм
  mark-and-sweep для поиска недостижимых циклов). Модуль `gc` — ручное
  управление (`gc.collect()`, `gc.disable()`, отслеживание объектов).
- **`weakref`** — слабые ссылки не увеличивают счётчик ссылок. Полезны для
  кешей и разрыва циклических ссылок без ожидания GC (например, ссылка
  "ребёнок → родитель" в дереве часто делается weak, чтобы не мешать сборке
  мусора родителя).
- **`is` vs `==`** — `is` сравнивает идентичность объектов (адрес в памяти,
  фактически id()), `==` — вызывает `__eq__`. В python/data-types.md уже
  разобран частный случай с кешированием маленьких int'ов
  ([пример](../python/data-types.md#example-int-memory)) — стоит явно обобщить это в
  отдельное правило "`is` для сравнения с `None`/singleton'ами, `==` — для
  сравнения значений".
- **Shallow copy vs deep copy** — `copy.copy()` копирует только верхний
  уровень контейнера (вложенные мутабельные объекты остаются общими),
  `copy.deepcopy()` рекурсивно копирует всё дерево объектов. Частая ловушка
  на собеседовании: `list(original)` / `original[:]` / `original.copy()` —
  тоже shallow copy.

## Ссылки

- [`gc` — Garbage Collector interface — официальная документация](https://docs.python.org/3/library/gc.html) — первоисточник по generational GC и ручному управлению.
- [`weakref` — Weak references — официальная документация](https://docs.python.org/3/library/weakref.html) — API и типичные сценарии использования.
- [`copy` — Shallow and deep copy operations — официальная документация](https://docs.python.org/3/library/copy.html) — точное определение разницы shallow/deep copy.
- [Python Memory Management: A Deep Dive into Reference Counting, Garbage Collection, and Real-World Leaks — Medium](https://devendra631995.medium.com/python-memory-management-a-deep-dive-into-reference-counting-garbage-collection-and-real-world-a9361cfa5f40) — сквозной разбор refcounting + GC с примерами утечек.
- [Python Memory Management and Weak References — UWPCE](https://uwpce-pythoncert.github.io/SystemDevelopment/weak_references.html) — учебный разбор weakref на практических примерах (кеши, деревья).
