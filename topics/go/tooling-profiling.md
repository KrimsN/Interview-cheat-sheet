# Go: инструменты, диагностика, профилирование

[🏠 Карта тем по Go](README.md)

## Что нужно знать

- **Тулчейн из коробки**: `go build`, `go run`, `go test`, `go fmt`
  (`gofmt`/`gofumpt`), `go vet`, `go doc`, `go generate`, `go mod`,
  `go work`, `go tool`. Отсутствие споров о форматировании — часть культуры.
- **Статический анализ**: `go vet` (проверки, почти не дающие ложных
  срабатываний: `printf`, `copylocks`, `lostcancel`, `loopclosure`),
  `staticcheck`, `golangci-lint` как агрегатор в CI.
- **Профили pprof** (`net/http/pprof` в сервисе или `go test -cpuprofile`):
  - **cpu** — где горит процессор;
  - **heap** — `inuse_space` (что живёт сейчас) vs `alloc_space` (что
    аллоцировалось всего) — разные вопросы, частая путаница;
  - **goroutine** — поиск утечек и зависших горутин, `?debug=2` даёт стеки;
  - **mutex** и **block** — конкуренция за блокировки и ожидание (нужно
    включать `runtime.SetMutexProfileFraction` / `SetBlockProfileRate`);
  - **threadcreate**, **allocs**.
  Просмотр: `go tool pprof -http=:8080 profile`, флейм-графики, `top`, `list`.
- **`go tool trace`** — временнáя развёртка: планировщик, паузы GC, блокировки
  сети и синхронизации. Отвечает на «почему latency растёт при нормальном CPU».
- **`GODEBUG`**: `gctrace=1`, `schedtrace=1000`, `scheddetail=1`,
  `madvdontneed`, `inittrace=1`. Полезно уметь назвать хотя бы `gctrace`.
- **Runtime-метрики**: пакет `runtime/metrics` (правильный современный
  способ), `runtime.ReadMemStats` (устаревающий, останавливает мир),
  экспорт в Prometheus.
- **Бенчмаркинг корректно**: `-benchtime`, `-count=10` + `benchstat` для
  статистической значимости, фиксация частоты CPU/шумных соседей.
- **Отладка**: `delve` (`dlv debug`, `dlv attach`), `runtime/debug.Stack()`,
  `debug.PrintStack()`, `debug.SetGCPercent`, `debug.SetMemoryLimit`,
  `GOTRACEBACK=all` для полных стеков при падении.
- **Сборка и артефакты**: кросс-компиляция `GOOS`/`GOARCH`, `CGO_ENABLED=0`
  для статического бинаря, `-trimpath` для воспроизводимых сборок,
  `-ldflags "-s -w"` для уменьшения размера, `go version -m binary` для
  просмотра встроенных версий зависимостей.
- **Безопасность цепочки поставок**: `govulncheck` (проверка по базе
  уязвимостей с учётом реально вызываемого кода), `go.sum` и `GONOSUMCHECK`,
  `go list -m -u all` для устаревших зависимостей.

## Ссылки

- [Diagnostics — go.dev](https://go.dev/doc/diagnostics) — карта всех средств диагностики: профили, трассировка, отладка, метрики.
- [Profiling Go Programs](https://go.dev/blog/pprof) — классическая статья про pprof на реальном примере оптимизации.
- [pkg.go.dev/net/http/pprof](https://pkg.go.dev/net/http/pprof) — как подключить профилирование к работающему сервису.
- [go tool trace — The Go Blog: More powerful Go execution traces](https://go.dev/blog/execution-traces-2024) — что показывает трассировка и как её читать.
- [govulncheck](https://go.dev/blog/govulncheck) — проверка зависимостей на известные уязвимости.
- [golangci-lint](https://golangci-lint.run/) — конфигурация набора линтеров для CI.
