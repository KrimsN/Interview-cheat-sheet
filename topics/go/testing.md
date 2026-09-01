# Go: тестирование

[🏠 Карта тем по Go](README.md)

## Что нужно знать

- **Стандартный пакет `testing`** без ассертов: `func TestX(t *testing.T)` в
  файле `*_test.go`. `t.Error/Errorf` — продолжить, `t.Fatal/Fatalf` — прервать
  тест (нельзя вызывать из другой горутины!), `t.Helper()` — чтобы номер
  строки указывал на вызывающего.
- **Table-driven tests** — идиома номер один: слайс структур-кейсов и
  `t.Run(tc.name, func(t *testing.T) {...})` для подтестов с именами и
  фильтрацией через `-run`.
- **Параллельные тесты**: `t.Parallel()`; до Go 1.22 требовалось копировать
  переменную цикла. Помните, что параллельные подтесты выполняются после
  выхода из родителя — отсюда ловушки с `defer` в родительском тесте
  (решение — `t.Cleanup`).
- **`t.Cleanup`, `t.TempDir`, `t.Setenv`, `t.Context`** (в свежих версиях) —
  стандартные средства изоляции вместо ручных `defer`.
- **`TestMain(m *testing.M)`** — глобальная подготовка (поднять контейнер,
  накатить миграции) и `os.Exit(m.Run())`.
- **Внешний и внутренний тест-пакет**: `package foo` (доступ к приватному) и
  `package foo_test` (только публичный API — заодно проверяет удобство API и
  разрывает циклы импортов).
- **Тестовые дублёры**: интерфейсы + ручные фейки — идиоматичный путь в Go;
  генерация моков (`mockery`, `gomock`) — когда интерфейсов много.
  Ключевая идиома: интерфейс объявляется у потребителя, поэтому мокать легко
  без DI-фреймворка.
- **Бенчмарки**: `func BenchmarkX(b *testing.B)` с циклом `for i := 0; i < b.N; i++`
  (в новых версиях — `for b.Loop()`), `b.ResetTimer`, `b.ReportAllocs`,
  `-benchmem`, сравнение результатов через `benchstat`. Не забыть про
  устранение мёртвого кода компилятором (запись результата в глобальную
  переменную).
- **Fuzzing** (Go 1.18+): `func FuzzX(f *testing.F)`, `f.Add` для сидов,
  `f.Fuzz(func(t *testing.T, data []byte) {...})`, корпус в `testdata/`.
- **Покрытие**: `go test -cover`, `-coverprofile` + `go tool cover -html`,
  покрытие интеграционных прогонов бинарника (`go build -cover`). Покрытие —
  метрика-индикатор, а не цель.
- **Флаги, о которых спрашивают**: `-race` (обязателен в CI), `-count=1`
  (обход кэша тестов), `-timeout`, `-short` + `testing.Short()`, `-v`, `-run`.
- **Интеграционные тесты**: `testcontainers-go`, `httptest.Server` и
  `httptest.NewRecorder` для HTTP, `net/http/httptest` вместо реальных портов.
- **Golden files** в `testdata/` (каталог игнорируется тулчейном) и флаг
  `-update` — идиома для тестов сериализации и рендеринга.

## Ссылки

- [pkg.go.dev/testing](https://pkg.go.dev/testing) — полный контракт `T`, `B`, `F`, `M` и всех флагов.
- [Go Wiki: TableDrivenTests](https://go.dev/wiki/TableDrivenTests) — канонический шаблон табличных тестов.
- [Using Subtests and Sub-benchmarks](https://go.dev/blog/subtests) — `t.Run`, параллельность, фильтрация.
- [Go Fuzzing](https://go.dev/doc/tutorial/fuzz) — официальный туториал по fuzz-тестам.
- [Code coverage for Go integration tests](https://go.dev/blog/integration-test-coverage) — покрытие за пределами unit-тестов.
- [Advanced Testing in Go — Mitchell Hashimoto (talk)](https://about.sourcegraph.com/blog/advanced-testing-in-go-with-mitchell-hashimoto) — практики тестирования больших Go-проектов.
