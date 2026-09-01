# `asyncio.TaskGroup`

[← GIL и конкурентность](concurrency-gil.md) · [🏠 Домой](../README.md) · [Базовый typing →](typing-basics.md)

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

Вложенность можно записать одной строкой — несколько менеджеров в одном
`async with` это ровно то же самое: `__aenter__` вызываются слева направо,
`__aexit__` — в обратном порядке (см. [Контекстные менеджеры](context-managers.md)).

```python
# python 3.11+
async with asyncio.timeout(5), asyncio.TaskGroup() as tg:
    tg.create_task(worker(1))
    tg.create_task(worker(2))
```

Обе формы дают одинаковый результат — на таймауте `0.5` c и задачах по `5` c:

```python
# one_with -> TimeoutError 0.51 c
# nested   -> TimeoutError 0.51 c
```

Если строка длинная, менеджеры берут в скобки и разбивают по строкам
(PEP 617, `python 3.10+`):

```python
# python 3.10+
async with (
    asyncio.timeout(5),
    asyncio.TaskGroup() as tg,
):
    tg.create_task(worker(1))
```

**Подвох.** Порядок менеджеров принципиален, и при ошибке ничего не падает —
таймаут просто перестаёт действовать:

```python
async with asyncio.TaskGroup() as tg, asyncio.timeout(0.5):
    tg.create_task(worker(1))          # задача на 5 секунд
# вышли без исключения через 5.01 c
```

Внутренний менеджер выходит первым: `asyncio.timeout.__aexit__` отрабатывает
сразу в конце тела блока, когда задачи только запущены. Ждёт их уже
`TaskGroup.__aexit__` — снаружи, где таймаута больше нет. Ни отмены, ни
`TimeoutError`, просто тихое ожидание все пять секунд.

Правило: `timeout` — снаружи (левее), `TaskGroup` — внутри (правее).

---

[← GIL и конкурентность](concurrency-gil.md) · [🏠 Домой](../README.md) · [Базовый typing →](typing-basics.md)
