# Go: методы и приёмники (receivers)

[🏠 Карта тем по Go](README.md)

## Что нужно знать

- **Метод — функция с приёмником**: `func (u User) Name() string`. Объявлять
  методы можно только для типов, определённых в **своём** пакете — нельзя
  добавить метод к `int` или к чужому типу (обход — свой defined type).
- **Value receiver vs pointer receiver** — вопрос почти на каждом интервью:
  - value receiver получает **копию**, мутации не видны снаружи;
  - pointer receiver позволяет менять состояние и не копирует большой объект;
  - если тип содержит `sync.Mutex` или другое некопируемое поле — только указатель;
  - **не смешивайте** value и pointer receiver у одного типа без причины.
- **Множество методов (method set)** — источник главной путаницы:
  у типа `T` в набор входят только методы с value receiver, у `*T` — и те, и
  другие. Поэтому **значение типа `T` не удовлетворяет интерфейсу, если метод
  объявлен на `*T`**, а `&t` — удовлетворяет. Компилятор при этом ругается на
  строке присваивания интерфейсу, а не в месте объявления метода.
- **Автоматическое взятие адреса** работает только для адресуемых значений:
  `t.PtrMethod()` компилируется для переменной, но не для элемента карты и не
  для результата функции.
- **Method values и method expressions**: `f := t.Method` (замыкание с уже
  привязанным приёмником, копия значения фиксируется в момент создания!) и
  `f := T.Method` (обычная функция, приёмник — первый аргумент). Ловушка:
  `defer t.Method()` с value receiver фиксирует копию `t` прямо сейчас.
- **Методы на nil-указателе легальны**: `func (l *List) Len() int` с проверкой
  `if l == nil { return 0 }` — рабочая идиома, а не UB.
- **Интерфейс vs конкретный тип в сигнатуре**: «принимай интерфейсы, возвращай
  структуры» — идиома Go, о ней спрашивают вместе с приёмниками.
- **Getters** не называют `GetX()` — идиоматично просто `X()`; сеттер `SetX()`.

## Ссылки

- [Go Spec: Method sets](https://go.dev/ref/spec#Method_sets) — формальное правило, из-за которого `T` и `*T` по-разному удовлетворяют интерфейсам.
- [Effective Go: Pointers vs. Values](https://go.dev/doc/effective_go#pointers_vs_values) — когда какой приёмник выбирать.
- [Go Code Review Comments: Receiver Type](https://go.dev/wiki/CodeReviewComments#receiver-type) — короткий чек-лист выбора приёмника от команды Go.
- [Go Spec: Method expressions](https://go.dev/ref/spec#Method_expressions) — семантика `T.Method` и `t.Method` как значений.
- [Methods, Interfaces and Embedded Types in Go — Ardan Labs](https://www.ardanlabs.com/blog/2014/05/methods-interfaces-and-embedded-types-in-golang.html) — разбор взаимодействия method sets, интерфейсов и встраивания.
