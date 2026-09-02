# Go — шпаргалка для собеседований

[🏠 Домой](../README.md) · [Базовый синтаксис и модель языка →](basics.md)

---

Темы в порядке чтения — от синтаксиса языка к конкурентности, рантайму и
практике. Каждая тема построена как «вопрос → ответ»: **Коротко** — модель
устного ответа, дальше разбор, рабочий пример с выводом, **Подвох** и
**Глубже**. Языконезависимая теория (ООП, SOLID, паттерны, архитектура,
конкурентность как концепция) — в [fundamentals/](../fundamentals/index.md).

### Язык

1. [Базовый синтаксис и модель языка](basics.md) — объявления, zero values, `iota`, `for range`, указатели
2. [Типы, константы, преобразования](types-constants.md) — defined types и алиасы, нетипизированные константы, `unsafe`
3. [Строки, байты, руны](strings-runes.md) — UTF-8, `len` в байтах, `strings.Builder`
4. [Массивы и слайсы](arrays-slices.md) — дескриптор, `len`/`cap`, ловушки `append`
5. [Карты](maps.md) — `nil`-карта, comma-ok, конкурентный доступ, `sync.Map`
6. [Структуры и встраивание](structs-embedding.md) — композиция вместо наследования, теги, функциональные опции
7. [Методы и приёмники](methods-receivers.md) — value vs pointer receiver, method set
8. [Интерфейсы](interfaces.md) — неявная реализация, устройство `iface`, ловушка «nil внутри интерфейса»
9. [Дженерики](generics.md) — параметры типов, ограничения, `~`
10. [Обработка ошибок](errors.md) — ошибки как значения, `%w`, `errors.Is/As`
11. [defer, panic, recover](defer-panic-recover.md) — LIFO, изменение именованных результатов

### Конкурентность

12. [Горутины и планировщик](goroutines-scheduler.md) — GMP, work stealing, вытеснение, утечки горутин
13. [Каналы и select](channels-select.md) — буферизация, `nil` и закрытые каналы, таймауты
14. [sync, atomic и модель памяти](sync-atomic.md) — мьютексы, `WaitGroup`, атомики, race detector
15. [context.Context](context.md) — отмена, дедлайны, значения
16. [Паттерны конкурентности](concurrency-patterns.md) — worker pool, pipeline, fan-in/fan-out, `errgroup`

### Рантайм и инструменты

17. [Память, стек, куча, GC](memory-gc.md) — escape analysis, аллокатор, трёхцветная разметка, `GOGC`/`GOMEMLIMIT`
18. [Модули, пакеты, сборка](modules-packages.md) — `go.mod`, MVS, `internal/`, build tags, кросс-компиляция
19. [Тестирование](testing.md) — табличные тесты, бенчмарки, fuzzing, `-race`, `httptest`
20. [Инструменты и профилирование](tooling-profiling.md) — `go vet`, pprof, trace, `GODEBUG`, `govulncheck`

### Практика

21. [Стандартная библиотека](stdlib-essentials.md) — `io`, `bufio`, `time`, `encoding/json`, `database/sql`
22. [HTTP-сервисы и сеть](http-servers.md) — `http.Handler`, мидлвари, таймауты, graceful shutdown
23. [Идиомы, стиль и архитектура проекта](idioms-style.md) — Effective Go, именование, раскладка каталогов
24. [Типовые вопросы и задачи](interview-questions.md) — чек-лист для самопроверки и задачи на живое кодирование

---

[🏠 Домой](../README.md) · [Базовый синтаксис и модель языка →](basics.md)
