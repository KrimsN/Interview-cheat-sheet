# Контекстные менеджеры: протокол, `contextlib`

[← Сортировка](sorting.md) · [🏠 Домой](../README.md) · [match / case →](pattern-matching.md)

---

## Что такое контекстный менеджер и как он устроен?

**Коротко.** Объект с методами `__enter__` и `__exit__`. `with` вызывает
первый на входе в блок, второй — на выходе, при любом исходе: обычном
завершении, `return`, `break` или исключении.

```python
class Ctx:
    def __enter__(self):
        print("enter")
        return self                       # это и попадёт в "as"
    def __exit__(self, exc_type, exc, tb):
        print("exit", exc_type)
        return False                      # исключение не подавляем

with Ctx() as c:
    raise ValueError("boom")
# enter
# exit <class 'ValueError'>
# ValueError: boom  — вылетело наружу
```

`__exit__` получает три аргумента — тип, значение и traceback исключения,
либо три `None`, если блок отработал без ошибки.

**Подвох.** `as` связывает то, что **вернул** `__enter__`, а не сам менеджер.
Классический пример: `with lock:` без `as`, потому что `Lock.__enter__`
возвращает `True`, а не сам объект блокировки.

---

## Как контекстный менеджер может подавить исключение?

**Коротко.** Вернув из `__exit__` истинное значение. Тогда исключение
считается обработанным и не распространяется дальше.

```python
class Swallow:
    def __enter__(self): return self
    def __exit__(self, *exc_info):
        return True                        # проглотили

with Swallow():
    raise ValueError("x")
print("alive")
# alive
```

Готовая реализация этого — `contextlib.suppress`, замена «пустому `except`»:

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    open("nope.txt")
```

**Подвох.** Молчаливое возвращение `True` из `__exit__` — источник тяжело
находимых багов: менеджер, написанный «для логирования», начинает глотать
все ошибки блока. Если явного `return` нет, функция вернёт `None` — ложное
значение, и это правильное поведение по умолчанию.

---

## Чем `with` лучше `try/finally`?

**Коротко.** Ничем по семантике — `with` и есть `try/finally`, но с логикой
захвата и освобождения, вынесенной в один переиспользуемый объект, а не
продублированной на каждом вызове.

```python
# эквивалент with open(...) as f:
f = open("data.txt")
try:
    data = f.read()
finally:
    f.close()
```

Несколько менеджеров в одном `with` — это вложенность, они закрываются
в обратном порядке:

```python
with open("in.txt") as src, open("out.txt", "w") as dst:
    dst.write(src.read())
```

**Глубже.** `finally` выполняется даже при `return` внутри `try`: значение уже
вычислено, но управление сначала пройдёт через `finally`. А `return` внутри
самого `finally` перетрёт и результат, и летящее исключение — поэтому так
никогда не пишут (с Python 3.14 это ещё и предупреждение компилятора,
PEP 765).

---

## Как сделать контекстный менеджер из функции?

**Коротко.** Декоратором `@contextlib.contextmanager` над генератором с одним
`yield`: всё до `yield` — это `__enter__`, всё после — `__exit__`, а сам
`yield` отдаёт значение в `as`.

```python
from contextlib import contextmanager

@contextmanager
def tag(name):
    print(f"<{name}>")
    try:
        yield name
    finally:
        print(f"</{name}>")

with tag("b") as t:
    print(t)
# <b>
# b
# </b>
```

**Подвох.** `try/finally` вокруг `yield` обязателен. Без него исключение из
тела `with` пробрасывается в генератор прямо в точку `yield`, код после него
не выполнится — и ресурс не освободится.

**Глубже.** Полезное из `contextlib`:

- `closing(obj)` — вызвать `obj.close()` на выходе для объектов без протокола;
- `ExitStack()` — динамическое количество менеджеров (список файлов, длина
  которого известна только в рантайме), `stack.enter_context(cm)`;
- `nullcontext(value)` — «пустой» менеджер, чтобы не ветвить код на
  `with`/без `with`;
- `@asynccontextmanager` и `async with` — те же протоколы `__aenter__`
  и `__aexit__` для asyncio (см. [`asyncio.TaskGroup`](asyncio-taskgroup.md),
  который сам является асинхронным контекстным менеджером).

Класс, реализующий протокол, к тому же переиспользуем: экземпляр
`@contextmanager`-генератора одноразовый, войти в него дважды нельзя.

---

[← Сортировка](sorting.md) · [🏠 Домой](../README.md) · [match / case →](pattern-matching.md)
