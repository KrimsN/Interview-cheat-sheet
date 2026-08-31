# Comprehensions vs генераторные выражения

## Что нужно знать

- **Виды comprehension** — list (`[x for x in it]`), dict
  (`{k: v for k, v in it}`), set (`{x for x in it}`), генераторное выражение
  (`(x for x in it)` — без квадратных скобок, лениво).
- **Память** — list/dict/set comprehension сразу материализуют всю
  коллекцию в памяти; генераторное выражение выдаёт элементы по одному
  (по сути — краткая запись функции-генератора, см.
  [Генератор](../python.md#генератор) в python.md). На больших
  последовательностях разница в памяти может быть многократной.
- **Скорость** — начиная с Python 3 list comprehension и генераторные
  выражения используют схожую реализацию и не сильно отличаются по
  скорости на итерацию; list comprehension обычно чуть быстрее там, где
  весь результат всё равно нужно материализовать, генератор — выигрывает,
  когда нужен только частичный проход (`any()`, `next()`, ранний `break`).
- **Вложенные comprehension** — `[x for row in matrix for x in row]` (плоский
  обход) и `[[x*y for x in row] for y in range(3)]` (вложенные списки) —
  частая путаница в порядке `for` при собеседовании: порядок такой же, как
  если бы это были обычные вложенные циклы `for`, читать слева направо.
- **Собственная область видимости** — начиная с Python 3, comprehension
  выполняется в отдельном скоупе (как маленькая функция), поэтому
  переменная-счётчик не "утекает" наружу и не перезаписывает одноимённую
  переменную во внешней области (в отличие от Python 2).

## Ссылки

- [List Comprehensions — официальный туториал Python](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions) — база от первоисточника, включая вложенные comprehension.
- [Generator expressions — официальная документация (PEP 289 в документации языка)](https://docs.python.org/3/reference/expressions.html#generator-expressions) — формальное описание генераторных выражений и их области видимости.
- [Python List Comprehensions vs Generator Expressions — GeeksforGeeks](https://www.geeksforgeeks.org/python-list-comprehensions-vs-generator-expressions/) — сравнение по памяти/скорости с конкретными цифрами.
