# Функциональный стиль: `*args`/`**kwargs`, `map`/`filter`/`reduce`, `functools.partial`

## Что нужно знать

- **`*args`/`**kwargs`** — сбор произвольного числа позиционных/именованных
  аргументов в функции. Важно уметь объяснить порядок параметров в сигнатуре
  (`def f(a, b, *args, c, **kwargs)`) и то, что после `*args` все параметры
  становятся keyword-only.
- **Распаковка при вызове** — `f(*list_)`, `f(**dict_)`, а также распаковка
  при присваивании (`a, *rest = [1, 2, 3]`) и объединение контейнеров
  (`{**d1, **d2}`, `[*l1, *l2]`).
- **`map`/`filter`** — `map(func, iterable)` возвращает итератор с
  результатом применения функции к каждому элементу, `filter(func, iterable)`
  — итератор с элементами, для которых функция вернула истину. Оба —
  ленивые (возвращают итератор, а не список).
- **`functools.reduce`** — в отличие от `map`/`filter`, не входит в builtins
  начиная с Python 3 (перенесён в `functools`), сворачивает
  последовательность в одно значение через бинарную функцию
  (`reduce(lambda acc, x: acc + x, items, 0)`). На собеседовании часто
  спрашивают, почему `reduce` "спрятали" в `functools` — Гвидо считал, что
  читаемость страдает, и в большинстве случаев лучше явный цикл или
  `sum`/`any`/`all`.
- **`functools.partial`** — "заморозка" части аргументов функции, создание
  специализированной версии без `lambda`. Отличие от `lambda`: partial
  сохраняет интроспекцию (`__wrapped__`-подобное поведение, доступ к
  исходной функции и зафиксированным аргументам через `.func`/`.args`/`.keywords`).
- **Когда не стоит использовать `lambda`** — присваивание lambda переменной
  (`f = lambda x: x + 1`) не рекомендуется PEP 8: лучше обычная `def`, так
  как это даёт нормальное имя в трейсбеках.

## Ссылки

- [`functools` — официальная документация](https://docs.python.org/3/library/functools.html) — первоисточник по `partial`, `reduce`, `lru_cache` и т.д. (часть уже используется в [декораторах python.md](../python.md#декораторы)).
- [Built-in Functions: `map`, `filter` — официальная документация](https://docs.python.org/3/library/functions.html) — точные сигнатуры и поведение при нескольких итерируемых объектах у `map`.
- [Understanding Python Partial Functions and Their Applications — Python Tutorial](https://www.pythontutorial.net/python-basics/python-partial-functions/) — практические примеры `functools.partial`.
