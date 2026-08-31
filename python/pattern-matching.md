# match / case (сопоставление с образцом)

[← Генератор](generators.md) · [🏠 Домой](../README.md) · [Группы исключений →](exception-groups.md)

---

`python 3.10+`. Аналог `switch`, но гораздо мощнее — умеет деструктурировать
структуры данных, проверять типы и накладывать условия (`guard`):

```python
# python 3.10+
def handle(command):
    match command.split():
        case ["go", direction] if direction in ("north", "south", "east", "west"):
            return f"go {direction}"
        case ["look"]:
            return "look around"
        case [action, *rest]:
            return f"{action} {rest}"
        case _:
            return "unknown command"
```

---

[← Генератор](generators.md) · [🏠 Домой](../README.md) · [Группы исключений →](exception-groups.md)
