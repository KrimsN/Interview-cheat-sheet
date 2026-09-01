# Go: карта тем для собеседования

Черновой раздел в формате `topics/`: по каждой теме — краткая выжимка
«что нужно знать» и подборка ссылок (официальная документация в приоритете,
дальше — проверенные разборы). Языконезависимая теория (ООП, SOLID, паттерны,
архитектура, конкурентность как концепция) лежит в
[fundamentals/](../../fundamentals/index.md) — здесь только то, что специфично
для Go.

## Порядок изучения

### Язык

1. [Базовый синтаксис и модель языка](basics.md) — объявления, zero values,
   `iota`, `for range`, указатели, «всё по значению».
2. [Типы, константы, преобразования](types-constants.md) — defined types и
   алиасы, нетипизированные константы, сравнимость, `unsafe`.
3. [Строки, байты, руны](strings-runes.md) — UTF-8, `len` в байтах,
   `strings.Builder`, `strconv`, глаголы `fmt`.
4. [Массивы и слайсы](arrays-slices.md) — дескриптор, `len`/`cap`, ловушки
   `append` и общего backing array, пакет `slices`.
5. [Карты](maps.md) — `nil`-карта, comma-ok, случайный порядок итерации,
   конкурентный доступ, `sync.Map`.
6. [Структуры и встраивание](structs-embedding.md) — композиция вместо
   наследования, теги, выравнивание, функциональные опции.
7. [Методы и приёмники](methods-receivers.md) — value vs pointer receiver,
   method sets, method values.
8. [Интерфейсы](interfaces.md) — неявная реализация, устройство iface,
   ловушка «`nil` внутри интерфейса», type switch, рефлексия.
9. [Дженерики](generics.md) — параметры типов, ограничения, `~`, границы
   применимости.
10. [Обработка ошибок](errors.md) — ошибки как значения, `%w`, `errors.Is/As`,
    когда паника уместна.
11. [defer, panic, recover](defer-panic-recover.md) — LIFO, вычисление
    аргументов, изменение именованных результатов.

### Конкурентность

12. [Горутины и планировщик](goroutines-scheduler.md) — GMP, work stealing,
    вытеснение, netpoller, `GOMAXPROCS`, утечки горутин.
13. [Каналы и select](channels-select.md) — буферизация, поведение `nil` и
    закрытых каналов, таймауты, направленные типы.
14. [sync, atomic и модель памяти](sync-atomic.md) — мьютексы, `WaitGroup`,
    `Once`, `Pool`, атомики, happens-before, race detector.
15. [context.Context](context.md) — отмена, дедлайны, значения, типовые ошибки.
16. [Паттерны конкурентности](concurrency-patterns.md) — worker pool,
    pipeline, fan-in/fan-out, `errgroup`, graceful shutdown, rate limiting.

### Рантайм и инструменты

17. [Память, стек, куча, GC](memory-gc.md) — escape analysis, аллокатор,
    трёхцветная разметка, `GOGC` и `GOMEMLIMIT`, «утечки» памяти.
18. [Модули, пакеты, сборка](modules-packages.md) — `go.mod`, MVS, semantic
    import versioning, `internal/`, build tags, кросс-компиляция, cgo.
19. [Тестирование](testing.md) — табличные тесты, подтесты, бенчмарки,
    fuzzing, покрытие, `-race`, `httptest`.
20. [Инструменты и профилирование](tooling-profiling.md) — `go vet`,
    `golangci-lint`, pprof, trace, `GODEBUG`, `govulncheck`.

### Практика

21. [Стандартная библиотека](stdlib-essentials.md) — `io`, `bufio`, `time`,
    `encoding/json`, `database/sql`, `log/slog`, `regexp`.
22. [HTTP-сервисы и сеть](http-servers.md) — `http.Handler`, мидлвари,
    таймауты, graceful shutdown, клиент и `Transport`, тестирование.
23. [Идиомы, стиль и архитектура проекта](idioms-style.md) — Effective Go,
    именование, раскладка каталогов, code smells.
24. [Типовые вопросы и задачи](interview-questions.md) — чек-лист для
    самопроверки и список задач на живое кодирование.

## Базовые источники по всему разделу

- [go.dev/doc](https://go.dev/doc/) — точка входа во всю официальную документацию.
- [The Go Programming Language Specification](https://go.dev/ref/spec) — спецификация языка целиком.
- [Effective Go](https://go.dev/doc/effective_go) — идиомы и стиль.
- [The Go Blog](https://go.dev/blog/all) — архив статей команды Go; большинство ссылок в темах ведут сюда.
- [pkg.go.dev/std](https://pkg.go.dev/std) — документация стандартной библиотеки.
- [Go by Example](https://gobyexample.com/) — короткие исполняемые примеры по всем конструкциям.
- [100 Go Mistakes](https://100go.co/) — типичные ошибки, удобно как финальная проверка перед интервью.
- [The Go Programming Language (Donovan, Kernighan)](https://www.gopl.io/) — основная книга по языку.
