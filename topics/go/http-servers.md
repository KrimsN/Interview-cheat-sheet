# Go: HTTP-сервисы и сеть

[🏠 Карта тем по Go](README.md)

## Что нужно знать

- **`http.Handler`** — интерфейс с `ServeHTTP(w, r)`; `http.HandlerFunc` —
  адаптер функции. Вся экосистема (мидлвари, роутеры, фреймворки) строится
  на этих двух сущностях — хороший пример силы маленького интерфейса.
- **Мидлварь** — функция `func(http.Handler) http.Handler`: логирование,
  recover, аутентификация, таймауты, CORS, метрики. Порядок обёртывания
  определяет порядок выполнения.
- **Роутинг**: `http.ServeMux` с Go 1.22 умеет методы и wildcards
  (`"POST /users/{id}"`, `r.PathValue("id")`) — часто снимает нужду во
  внешнем роутере. Из популярных: `chi`, `gin`, `echo`, `fiber` (не на
  `net/http`), gRPC для внутренних сервисов.
- **Каждый запрос — своя горутина**, поэтому общее состояние хендлеров должно
  быть потокобезопасным. `r.Context()` отменяется при разрыве соединения.
- **Таймауты сервера обязательны**: `ReadHeaderTimeout`, `ReadTimeout`,
  `WriteTimeout`, `IdleTimeout`, `MaxHeaderBytes`. Сервер по умолчанию их не
  имеет — классический вопрос про уязвимость к Slowloris.
- **Graceful shutdown**: `signal.NotifyContext` → `srv.Shutdown(ctx)` с
  таймаутом; понимать разницу с `Close()`.
- **HTTP-клиент**: **не используйте `http.DefaultClient` в проде** —
  у него нет таймаута. Свой `http.Client{Timeout: ...}` + настроенный
  `http.Transport` (`MaxIdleConnsPerHost`, `IdleConnTimeout`),
  переиспользование клиента (он потокобезопасен), обязательные
  `defer resp.Body.Close()` **и** дочитывание тела (`io.Copy(io.Discard, body)`)
  для переиспользования соединения — типичный источник «утечки» соединений.
- **Ошибки и статусы**: `w.WriteHeader` можно вызвать один раз и до записи
  тела; `http.Error`, `http.StatusText`. Ответ с ошибкой после начала записи
  тела уже невозможен.
- **Тестирование**: `httptest.NewRecorder` для хендлеров, `httptest.NewServer`
  для клиентов, подмена `Transport` через `RoundTripper` — идиоматичный мок.
- **Работа с телом**: `json.NewDecoder(r.Body)` vs `io.ReadAll`,
  `http.MaxBytesReader` для защиты от больших тел, multipart-формы.
- **Стриминг и long-polling**: `http.Flusher`, SSE, `http.ResponseController`
  (Go 1.20+) для per-request таймаутов; WebSocket через `gorilla/websocket`
  или `nhooyr/coder websocket`.
- **HTTP/2 включён автоматически при TLS**; `h2c` требует явной настройки.
- **Наблюдаемость**: OpenTelemetry-мидлварь, `httptrace`, метрики RED,
  проброс trace id через `context`.

## Ссылки

- [pkg.go.dev/net/http](https://pkg.go.dev/net/http) — контракты `Server`, `Client`, `Transport`, все поля таймаутов.
- [Routing Enhancements for Go 1.22](https://go.dev/blog/routing-enhancements) — методы и wildcards в стандартном `ServeMux`.
- [Writing Web Applications](https://go.dev/doc/articles/wiki/) — официальный туториал по `net/http` с нуля.
- [The complete guide to Go net/http timeouts — Cloudflare](https://blog.cloudflare.com/the-complete-guide-to-golang-net-http-timeouts/) — эталонный разбор всех таймаутов клиента и сервера.
- [pkg.go.dev/net/http/httptest](https://pkg.go.dev/net/http/httptest) — тестирование хендлеров и клиентов.
- [gRPC-Go](https://grpc.io/docs/languages/go/quickstart/) — альтернативный транспорт для межсервисного взаимодействия.
