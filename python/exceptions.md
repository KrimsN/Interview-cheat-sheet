# Исключения: иерархия, `try/except/else/finally`, `raise ... from ...`

[← match / case](pattern-matching.md) · [🏠 Домой](../README.md) · [Группы исключений →](exception-groups.md)

---

## Почему `except Exception` не ловит `KeyboardInterrupt`?

**Коротко.** Потому что `KeyboardInterrupt` наследуется не от `Exception`,
а напрямую от `BaseException` — как и всё, что означает «программа должна
завершиться», а не «в программе ошибка».

```python
BaseException.__subclasses__()
# [BaseExceptionGroup, Exception, GeneratorExit, KeyboardInterrupt, SystemExit]
```

- `SystemExit` — вызван `sys.exit()`;
- `KeyboardInterrupt` — пользователь нажал Ctrl+C;
- `GeneratorExit` — генератор закрывают (см. [Генератор](generators.md));
- `Exception` — всё остальное, то есть обычные ошибки прикладного кода.

Разделение сделано ровно затем, чтобы широкий `except Exception:` в цикле
обработки задач не мешал завершить процесс.

**Подвох.** Голый `except:` эквивалентен `except BaseException:` и ловит в том
числе Ctrl+C — из-за этого программу нельзя остановить. Это антипаттерн,
линтеры помечают его отдельным правилом (`E722`).

**Глубже.** Порядок `except`-веток важен: проверяются они сверху вниз, и первая
подходящая по `isinstance` выигрывает. Поэтому общие исключения ставят ниже
специфичных, иначе нижние ветки станут недостижимы — синтаксической ошибкой
это не считается, компилятор не предупредит.

---

## Зачем в `try` нужны `else` и `finally`?

**Коротко.** `else` выполняется, только если исключения не было; `finally` —
всегда. `else` сужает зону, которую защищает `except`, а `finally` гарантирует
освобождение ресурса.

```python
def read(x):
    try:
        r = 10 / x
    except ZeroDivisionError as e:
        print("except:", e)
        return None
    else:
        print("else")
        return r
    finally:
        print("finally")

read(2)
# else
# finally
# -> 5.0
```

Без `else` весь «успешный» код пришлось бы держать внутри `try`, где его
собственные ошибки случайно попали бы в тот же `except`.

**Подвох.** `finally` отрабатывает и при `return`/`break` внутри `try`:
значение уже вычислено, но управление всё равно пройдёт через `finally`.
А `return` в самом `finally` перетирает результат и **гасит летящее
исключение**:

```python
def g():
    try:
        return "try"
    finally:
        return "finally"

g()
# 'finally'
```

С Python 3.14 такой код даёт `SyntaxWarning` (PEP 765). На практике
`try/finally` для ресурсов почти всегда лучше заменить на
[контекстный менеджер](context-managers.md).

**Глубже.** Переменная из `except ... as e` удаляется по выходу из блока —
интерпретатор дописывает `del e`, чтобы traceback в `e` не удерживал ссылками
целый кадр стека. Обращение к `e` после блока даёт `NameError`; если значение
нужно дальше, его копируют в другое имя.

---

## Чем `raise ... from ...` отличается от простого `raise`?

**Коротко.** `from` явно задаёт причину (`__cause__`) — «это исключение вызвано
вот тем». Без `from` контекст всё равно сохранится, но как неявный
(`__context__`), и формулировка в traceback будет другой.

```python
try:
    try:
        1 / 0
    except ZeroDivisionError as e:
        raise ValueError("bad config") from e
except ValueError as e:
    type(e.__cause__)               # <class 'ZeroDivisionError'>
    e.__context__ is e.__cause__    # True
```

В traceback это две разные фразы:

- `from` → «The above exception was the direct cause of the following exception»;
- без `from` → «During handling of the above exception, another exception occurred».

`raise ... from None` подавляет цепочку целиком (`__suppress_context__ = True`) —
это уместно, когда внутренняя ошибка деталь реализации и только шумит
в логе.

**Подвох.** Голый `raise` внутри `except` — не то же самое, что
`raise ТипОшибки(...)`: он пробрасывает **текущее** исключение с исходным
traceback, не создавая нового объекта. Это правильный способ «залогировать
и пробросить дальше».

---

## Как правильно объявлять свои исключения?

**Коротко.** Наследуются от `Exception` (или от более специфичного
встроенного класса), а не от `BaseException`, и заводят один общий корень
на приложение — чтобы вызывающий код мог поймать «любую нашу ошибку»
одной веткой.

```python
class AppError(Exception):
    """Базовая ошибка приложения."""

class ConfigError(AppError): ...
class RetryableError(AppError): ...

try:
    load()
except RetryableError:
    retry()
except AppError:
    fail()
```

Иерархию строят от того, **как ошибку будут обрабатывать**, а не от того, где
она возникла: если два класса всегда ловят вместе — они не должны быть
разными классами.

**Глубже.** Наследование от встроенных типов работает и как совместимость:
`class MyKeyError(AppError, KeyError)` поймается и старым кодом с
`except KeyError`. Так же поступила и стандартная библиотека при введении
`OSError` в Python 3.3 — старые `IOError`, `EnvironmentError`, `socket.error`
стали его псевдонимами.

Следующий уровень — когда ошибок сразу несколько (конкурентные задачи):
для этого есть [`ExceptionGroup` и `except*`](exception-groups.md).

---

[← match / case](pattern-matching.md) · [🏠 Домой](../README.md) · [Группы исключений →](exception-groups.md)
