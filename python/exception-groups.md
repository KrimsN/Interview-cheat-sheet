# Группы исключений: `except*` и `ExceptionGroup`

[← match / case](pattern-matching.md) · [🏠 Домой](../README.md) · [asyncio.TaskGroup →](asyncio-taskgroup.md)

---

`python 3.11+`. Позволяет "поднять" сразу несколько исключений одновременно
(актуально для конкурентного кода, [`asyncio.TaskGroup`](asyncio-taskgroup.md) и
т.д.) и обрабатывать их по типам:

```python
# python 3.11+
try:
    raise ExceptionGroup("group", [OSError("io"), ValueError("val")])
except* OSError:
    print("были OSError")
except* ValueError:
    print("были ValueError")
```

---

[← match / case](pattern-matching.md) · [🏠 Домой](../README.md) · [asyncio.TaskGroup →](asyncio-taskgroup.md)
