# `tomllib`

[← Тайпинг](typing-advanced.md) · [🏠 Домой](../README.md) · [Классы: dataclasses, enum →](classes-dataclasses-enum.md)

---

## Как читать TOML без сторонних библиотек?

**Коротко.** `python 3.11+` — парсер TOML встроен в стандартную библиотеку.
Только чтение: `load()` и `loads()`, записи нет.

TOML в экосистеме Python — это прежде всего `pyproject.toml`, поэтому парсер и
затащили в stdlib.

```python
# python 3.11+
import tomllib

with open("pyproject.toml", "rb") as f:      # обязательно "rb"
    config = tomllib.load(f)

tomllib.loads('a = 1')      # {'a': 1}
```

**Подвох.** Файл нужно открывать **в бинарном режиме**. В отличие от `json.load`,
который спокойно работает с текстовым файлом, `tomllib.load` на текстовом
режиме падает:

```python
tomllib.load(open("pyproject.toml"))
# TypeError: File must be opened in binary mode, e.g. use `open('foo.toml', 'rb')`
```

Так сделано намеренно: спецификация TOML требует UTF-8, и бинарный режим не даёт
операционной системе подставить другую кодировку по умолчанию.

**Глубже.** Для записи TOML стандартной библиотеки нет — нужен сторонний
`tomli-w`. Для более старых версий Python обратно совместимый парсер называется
`tomli` (`tomllib` — это буквально он, принятый в stdlib).

---

[← Тайпинг](typing-advanced.md) · [🏠 Домой](../README.md) · [Классы: dataclasses, enum →](classes-dataclasses-enum.md)
