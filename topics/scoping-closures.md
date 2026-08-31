# Область видимости: LEGB, замыкания, `nonlocal`/`global`, late binding

## Что нужно знать

- **Правило LEGB** — порядок поиска имени: **L**ocal (текущая функция) →
  **E**nclosing (объемлющая функция, если есть вложенность) → **G**lobal
  (уровень модуля) → **B**uilt-in (встроенные имена `len`, `print` и т.д.).
- **Замыкания (closures)** — функция "помнит" переменные из объемлющей
  области видимости даже после того, как та завершила выполнение. Технически
  это `__closure__` — кортеж cell-объектов, каждый из которых хранит
  ссылку (не значение!) на захваченную переменную.
- **`nonlocal` vs `global`** — по умолчанию присваивание внутри функции
  создаёт новую локальную переменную, а не изменяет внешнюю. `global`
  используется для изменения переменной уровня модуля, `nonlocal` — для
  изменения переменной объемлющей (но не глобальной) функции. Без них
  попытка присвоить значение "внешней" переменной внутри функции приводит
  к `UnboundLocalError`, если переменная с тем же именем читается раньше
  присваивания.
- **Late binding в замыканиях — классическая ловушка**: замыкание
  захватывает не значение переменной на момент создания функции, а ссылку
  на саму переменную. Поэтому все замыкания, созданные в цикле, в момент
  вызова видят одно и то же (последнее) значение переменной цикла:

  ```python
  funcs = [lambda: i for i in range(3)]
  [f() for f in funcs]
  # [2, 2, 2], а не [0, 1, 2] — как многие ожидают

  # Фикс — зафиксировать значение через параметр по умолчанию:
  funcs = [lambda i=i: i for i in range(3)]
  [f() for f in funcs]
  # [0, 1, 2]
  ```

## Ссылки

- [Python Scope and the LEGB Rule: Resolving Names in Your Code — Real Python](https://realpython.com/python-scope-legb-rule/) — подробный разбор LEGB с примерами и `nonlocal`/`global`.
- [Python Closures: Lexical Scope, Late Binding, and Decorators — FaceP](https://faceprep.in/article/closures-in-python-face-prep/) — связка "замыкания + декораторы + late binding" в одном месте.
- [Python Late Binding in Closures: A Common Bug and How to Avoid It — OpenPython](https://openpython.org/articles/python-closure-loop-variable-bug) — целиком про ловушку с циклом и способы её обхода.
