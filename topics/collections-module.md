# Модуль `collections`: `defaultdict`, `Counter`, `deque`, `namedtuple`

## Что нужно знать

- **`Counter`** — подкласс `dict` для подсчёта хешируемых объектов
  (`Counter(words)`). Полезные методы: `.most_common(n)`, поддержка
  арифметики между счётчиками (`c1 + c2`, `c1 - c2`).
- **`defaultdict`** — подкласс `dict`, который при обращении к
  отсутствующему ключу вызывает фабрику по умолчанию (`defaultdict(list)`,
  `defaultdict(int)`) вместо `KeyError`. Убирает необходимость в
  `if key not in d: d[key] = ...`.
- **`deque`** — двусторонняя очередь с O(1) добавлением/удалением с обоих
  концов (в отличие от `list`, где `insert(0, x)`/`pop(0)` — O(n)). Есть
  `maxlen` для реализации кольцевого буфера / "последние N элементов".
- **`namedtuple`** — лёгкий неизменяемый класс-запись с именованными полями
  поверх обычного `tuple`, без накладных расходов полноценного класса.
  Стоит уметь сравнить с [`dataclass`](../python/classes-dataclasses-enum.md)
  (namedtuple — immutable и легче, dataclass — гибче, поддерживает
  мутабельность/методы/значения по умолчанию).
- **`OrderedDict`** — до Python 3.7 был единственным способом гарантировать
  порядок ключей в словаре; начиная с 3.7 обычный `dict` сохраняет порядок
  вставки как часть спецификации языка. `OrderedDict` сейчас нужен, только
  если важны специфичные операции (`move_to_end()`, сравнение с учётом
  порядка при `==`).

## Ссылки

- [`collections` — официальная документация](https://docs.python.org/3/library/collections.html) — первоисточник по всем типам модуля, включая `ChainMap` и `UserDict`.
- [collections | Python Standard Library — Real Python](https://realpython.com/ref/stdlib/collections/) — краткий справочник с примерами по каждому типу.
- [Python collections Module: Counter, defaultdict & deque — OpenPython](https://openpython.org/articles/python-collections-module-guide) — практический разбор с типовыми задачами (подсчёт слов, кольцевой буфер и т.д.).
