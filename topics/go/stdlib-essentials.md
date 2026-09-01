# Go: стандартная библиотека — что нужно знать

[🏠 Карта тем по Go](README.md)

## Что нужно знать

- **`io`** — фундамент: `Reader`, `Writer`, `Closer`, `ReaderFrom`,
  `WriterTo`, `io.Copy` (и почему он не аллоцирует буфер, если тип умеет
  `ReadFrom`/`WriteTo`), `io.LimitReader`, `io.MultiWriter`, `io.Pipe`,
  `io.EOF` как ожидаемое, а не ошибочное состояние.
- **`bufio`** — буферизация, `Scanner` для построчного чтения (и его лимит
  `bufio.MaxScanTokenSize`, из-за которого «длинные строки теряются»),
  `Reader.ReadString`, `Writer.Flush` (забытый `Flush` — классический баг).
- **`os` и `path/filepath`** — файлы, переменные окружения, `os.ReadFile`/
  `WriteFile`, `os.Signal`, различие `path` (URL-подобные) и `filepath`
  (ОС-зависимые разделители), `io/fs` и `os.DirFS`, `//go:embed`.
- **`encoding/json`** — теги, `omitempty` (и что он не различает «ноль» и
  «не задано» — отсюда указатели или `json.RawMessage`), `Marshaler`/
  `Unmarshaler`, `json.Decoder` для потоков, `DisallowUnknownFields`,
  числа как `float64` в `map[string]any`, регистронезависимый матчинг полей.
  Знать про `encoding/json/v2` как направление развития.
- **`time`** — `Time` (монотонные часы внутри! `Sub` корректно работает при
  переводе стенных часов), `Duration` как `int64` наносекунд, `Timer`,
  `Ticker` (обязательный `Stop`), `time.After` в цикле как источник мусора,
  форматирование по опорному времени `2006-01-02 15:04:05`, таймзоны и `UTC`.
- **`net/http`** — клиент и сервер; см. отдельную тему
  [HTTP-сервисы](http-servers.md).
- **`database/sql`** — пул соединений (`SetMaxOpenConns`, `SetMaxIdleConns`,
  `SetConnMaxLifetime`), обязательный `rows.Close()` и `rows.Err()`,
  `QueryContext`, `sql.NullString`/указатели, плейсхолдеры вместо
  конкатенации (SQL-инъекции), транзакции и `defer tx.Rollback()`.
- **`log/slog`** (Go 1.21+) — структурное логирование: хендлеры, уровни,
  `slog.With`, контекстные атрибуты. Заменяет `log` в новых проектах.
- **`sort`, `slices`, `maps`, `cmp`** — современный порядок: `slices.SortFunc`
  вместо `sort.Slice`, `cmp.Compare`, `slices.BinarySearch`.
- **`regexp`** — RE2: линейное время, **нет backreferences и lookahead** —
  частый вопрос «почему мой regexp не работает». Компилировать один раз
  (`MustCompile` в глобальной переменной).
- **`context`, `sync`, `errors`** — см. соответствующие темы.
- **`math/rand` vs `crypto/rand`**: первый не криптостойкий (с Go 1.20
  автоматически засеян, `rand/v2` — современный API), второй — для токенов и
  паролей.
- **`net`** — `Dialer` с таймаутами, DNS, `net.Conn`, `net.Listener`.
- **`encoding/*`**: `csv`, `xml`, `base64`, `hex`, `gob`, `binary`
  (порядок байтов).

## Ссылки

- [Standard library index](https://pkg.go.dev/std) — полный список пакетов; полезно пройтись глазами перед интервью.
- [JSON and Go](https://go.dev/blog/json) — маршалинг, теги, `RawMessage`, потоковый декодер.
- [pkg.go.dev/io](https://pkg.go.dev/io) — контракты `Reader`/`Writer`, на которых построена вся библиотека.
- [pkg.go.dev/time](https://pkg.go.dev/time) — монотонные часы, `Timer`/`Ticker`, формат опорного времени.
- [pkg.go.dev/database/sql](https://pkg.go.dev/database/sql) и [Go database/sql tutorial](http://go-database-sql.org/) — пул соединений и типичные ошибки работы с БД.
- [Structured Logging with slog](https://go.dev/blog/slog) — модель и производительность `log/slog`.
- [RE2 syntax](https://github.com/google/re2/wiki/Syntax) — что поддерживает `regexp` и чего в нём принципиально нет.
