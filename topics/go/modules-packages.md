# Go: модули, пакеты, сборка

[🏠 Карта тем по Go](README.md)

## Что нужно знать

- **Пакет — единица компиляции и инкапсуляции**, каталог = пакет. Имя пакета
  короткое и без подчёркиваний (`http`, не `http_utils`); имя не дублируется в
  идентификаторах (`http.Server`, а не `http.HTTPServer`).
- **`init()`** выполняется после инициализации переменных пакета, до `main`;
  их может быть несколько в пакете, порядок между файлами — по имени файла.
  Импорт ради побочного эффекта — `import _ "github.com/lib/pq"`.
- **Циклические импорты запрещены** на уровне компилятора — это дисциплинирует
  архитектуру; типичное лечение — вынести общий интерфейс или тип в третий пакет.
- **`internal/`** — пакеты внутри видны только поддереву родителя `internal`;
  единственный настоящий механизм ограничения видимости между пакетами.
- **Модули**: `go.mod` (`module`, `go`, `require`, `replace`, `exclude`,
  `toolchain`), `go.sum` (хеши для проверки целостности). `go mod tidy`,
  `go mod why`, `go mod graph`, `go mod vendor`.
- **MVS (minimal version selection)** — Go выбирает **минимальную** версию,
  удовлетворяющую всем требованиям, а не максимальную. Это отличает Go от
  npm/pip и часто спрашивается.
- **Semantic Import Versioning**: мажорная версия ≥ v2 входит в путь импорта
  (`example.com/mod/v2`). Причина — возможность держать две мажорные версии
  в одном бинарнике.
- **Псевдоверсии** (`v0.0.0-20240101120000-abcdef123456`) для коммитов без тега.
- **Прокси и приватные модули**: `GOPROXY` (по умолчанию `proxy.golang.org`),
  `GOSUMDB`, `GOPRIVATE`/`GONOSUMDB`, `GOFLAGS=-mod=mod|readonly`.
- **Workspaces** (`go.work`, Go 1.18+) — разработка нескольких модулей
  одновременно без `replace`.
- **Сборка**: `go build`, `go install`, кросс-компиляция через `GOOS`/`GOARCH`
  без тулчейна, статические бинарники (и почему `CGO_ENABLED=0` даёт
  по-настоящему статический бинарь для scratch-образа), `-ldflags "-s -w
  -X main.version=..."` для версии в бинарнике.
- **Build tags / constraints**: `//go:build linux && amd64`, суффиксы файлов
  `_linux.go`, `_test.go`. Директивы `//go:embed`, `//go:generate`.
- **cgo** — знать цену: теряется кросс-компиляция «из коробки», дорогие
  переходы Go↔C, отдельный поток на блокирующий вызов.

## Ссылки

- [Go Modules Reference](https://go.dev/ref/mod) — полный справочник: MVS, semantic import versioning, прокси, `go.sum`.
- [Managing dependencies](https://go.dev/doc/modules/managing-dependencies) — практика повседневной работы с зависимостями.
- [Organizing a Go module](https://go.dev/doc/modules/layout) — официальные рекомендации по структуре модуля, включая `internal/` и `cmd/`.
- [Effective Go: Package names](https://go.dev/blog/package-names) — правила именования пакетов и API.
- [Tutorial: Get started with multi-module workspaces](https://go.dev/doc/tutorial/workspaces) — `go.work` на практике.
- [go command documentation](https://pkg.go.dev/cmd/go) — все подкоманды, build tags, переменные окружения.
