# `asyncio.TaskGroup`

[← Группы исключений](exception-groups.md) · [🏠 Домой](../README.md) · [Тайпинг →](typing-advanced.md)

---

`python 3.11+`. Замена паттерна `asyncio.gather()` со структурированной
конкурентностью: если одна из задач упадёт, остальные будут отменены, а
исключения соберутся в [`ExceptionGroup`](exception-groups.md):

```python
# python 3.11+
import asyncio

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(worker(1))
        tg.create_task(worker(2))
```

---

[← Группы исключений](exception-groups.md) · [🏠 Домой](../README.md) · [Тайпинг →](typing-advanced.md)
