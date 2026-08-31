# `asyncio.TaskGroup`

[← Группы исключений](exception-groups.md) · [🏠 Домой](../README.md) · [Тайпинг →](typing-advanced.md)

---

## Чем `TaskGroup` лучше `asyncio.gather()`?

**Коротко.** `python 3.11+`. Это структурированная конкурентность: группа не
выпустит управление, пока не завершатся все задачи, а при падении одной —
отменит остальные и соберёт ошибки в
[`ExceptionGroup`](exception-groups.md).

```python
# python 3.11+
import asyncio

async def worker(n):
    await asyncio.sleep(0.01)
    if n == 2:
        raise ValueError(f"worker {n} упал")
    return n

async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            for i in (1, 2, 3):
                tg.create_task(worker(i))
    except* ValueError as eg:
        print([str(x) for x in eg.exceptions])
        # ['worker 2 упал']

asyncio.run(main())
```

Разница с `gather()` видна на долгой соседней задаче: `TaskGroup` отменяет её
сразу, `gather()` — оставляет работать в фоне.

```python
async def slow():
    await asyncio.sleep(5)        # с TaskGroup будет отменена через 0.02 c
```

**Подвох.** У `gather(..., return_exceptions=True)` ошибки не поднимаются вовсе —
они возвращаются в списке результатов вперемешку со значениями, и их легко
случайно не проверить. `TaskGroup` так «проглотить» ошибку не даёт.

**Глубже.** Добавлять задачи через `create_task()` можно только внутри блока
`async with` — после выхода группа закрыта, и попытка даст `RuntimeError`. Это и
есть суть структурированной конкурентности: время жизни задач не может пережить
блок, в котором они созданы, поэтому «потерянных» задач не остаётся.

---

## Как ограничить время выполнения?

**Коротко.** `python 3.11+` — контекстный менеджер `asyncio.timeout()`, обычно
используется вместе с `TaskGroup`.

```python
# python 3.11+
async with asyncio.timeout(5):
    async with asyncio.TaskGroup() as tg:
        tg.create_task(worker(1))
        tg.create_task(worker(2))
```

По истечении срока задачи отменяются, а наружу выходит `TimeoutError`. В отличие
от старого `asyncio.wait_for`, таймаут задаётся на блок кода, а не на одну
корутину.

---

[← Группы исключений](exception-groups.md) · [🏠 Домой](../README.md) · [Тайпинг →](typing-advanced.md)
