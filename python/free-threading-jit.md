# CPython без GIL: free-threading, JIT и суб-интерпретаторы

[← Классы: dataclasses, enum](classes-dataclasses-enum.md) · [🏠 Домой](../README.md) · [Инструменты разработчика →](dev-tools.md)

---

**Free-threading (no-GIL)** — в `python 3.13` появилась экспериментальная
сборка CPython без GIL (`python3.13t`, PEP 703), не включена по умолчанию, и
часть экосистемы (расширения на C) ещё не полностью совместима. В
`python 3.14+` (PEP 779) free-threaded сборка перестала считаться
"экспериментальной" и получила статус официально поддерживаемой (хотя
по-прежнему не является сборкой по умолчанию — стандартный `python`
собирается с GIL, free-threaded ставится отдельно, например
`python3.14t` / `uv python install 3.14t`).

Проверить, в какой сборке вы находитесь, можно прямо из кода:

```python
import sys, sysconfig
sys._is_gil_enabled()                      # True в обычной сборке
sysconfig.get_config_var("Py_GIL_DISABLED")  # 0 в обычной, 1 во free-threaded
```

**Экспериментальный JIT** (`python 3.13+`, PEP 744) — добавлен
copy-and-patch JIT-компилятор, отключённый по умолчанию (нужна сборка с
`--enable-experimental-jit`). Пока не даёт заметного прироста
производительности "из коробки" — это фундамент под будущие версии.

**Мультиинтерпретаторы в stdlib** (`python 3.14+`, PEP 734) — модуль
`concurrent.interpreters` даёт доступ к нескольким изолированным
суб-интерпретаторам CPython (каждый со своим GIL/состоянием) прямо из
стандартной библиотеки — раньше эта возможность существовала только в C API.
Ещё один инструмент для параллелизма в обход одного общего GIL, отдельно от
free-threading.

---

[← Классы: dataclasses, enum](classes-dataclasses-enum.md) · [🏠 Домой](../README.md) · [Инструменты разработчика →](dev-tools.md)
