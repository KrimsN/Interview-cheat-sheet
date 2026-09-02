# HTTP-сервисы и сеть

[← Стандартная библиотека](stdlib-essentials.md) · [🏠 Домой](../README.md) · [Идиомы, стиль и архитектура →](idioms-style.md)

---

## На чём построен `net/http`, и как работают мидлвари?

**Коротко.** Весь сервер стоит на одном однометодном интерфейсе —
`http.Handler` с методом `ServeHTTP(w http.ResponseWriter, r *http.Request)`.
`http.HandlerFunc` — тип-адаптер, который превращает обычную функцию в
`Handler`, реализуя тот же метод как вызов самой себя.

```go
type Handler interface {
    ServeHTTP(ResponseWriter, *Request)
}

type HandlerFunc func(ResponseWriter, *Request)

func (f HandlerFunc) ServeHTTP(w ResponseWriter, r *Request) {
    f(w, r)
}
```

Мидлварь — это просто функция, которая принимает `Handler` и возвращает новый
`Handler`, оборачивающий исходный дополнительным поведением: `func(http.
Handler) http.Handler`. Роутеры, фреймворки (`chi`, `gin`) и весь экосистемный
инструментарий логирования/метрик/аутентификации строятся поверх этих двух
определений — хороший пример того, как маленький интерфейс в Go покрывает
целую экосистему.

```go
func withLogging(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        log.Printf("%s %s %s", r.Method, r.URL.Path, time.Since(start))
    })
}

func withRecover(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if rec := recover(); rec != nil {
                log.Printf("panic: %v", rec)
                http.Error(w, "internal error", http.StatusInternalServerError)
            }
        }()
        next.ServeHTTP(w, r)
    })
}

handler := withRecover(withLogging(mux))
```

Порядок оборачивания определяет порядок выполнения: `withRecover(withLogging(
mux))` значит «сначала ловим панику вокруг всего, затем логируем, затем сам
обработчик» — `withRecover` должен быть снаружи, иначе паника внутри
`withLogging` не будет перехвачена.

**Подвох.** Каждый входящий запрос обслуживается в **своей** горутине —
поэтому любое общее состояние, к которому обращается хендлер (счётчики, кэши,
клиенты БД), обязано быть потокобезопасным. Локальные переменные внутри
`ServeHTTP` в порядке — они видны только текущему запросу.

---

## Что изменилось в маршрутизации `net/http` в Go 1.22?

**Коротко.** До Go 1.22 стандартный `http.ServeMux` умел сопоставлять только
префиксы пути, без методов и параметров — отсюда популярность внешних
роутеров. С Go 1.22 `ServeMux` научился методам и wildcard-сегментам прямо в
шаблоне маршрута.

```go
// go 1.22+
mux := http.NewServeMux()
mux.HandleFunc("GET /users/{id}", func(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    fmt.Fprintf(w, "user %s", id)
})
mux.HandleFunc("POST /users", createUser)
mux.HandleFunc("GET /files/{path...}", serveFile) // {name...} — «хвост» пути
```

Правила приоритета: более специфичный шаблон побеждает более общий
(`/users/{id}` предпочтительнее `/users/`), а точный литеральный сегмент —
wildcard того же места. Это снимает необходимость во внешнем роутере для
многих сервисов, хотя `chi`, `gin`, `echo` остаются полезны там, где нужны
группировка мидлварей на уровне поддерева маршрутов, встроенная валидация
или биндинг тела запроса. `fiber` стоит особняком — он не построен на
`net/http`, а использует `fasthttp`, что даёт скорость, но ломает
совместимость с частью стандартной экосистемы (`http.Handler`,
`httptest`).

**Подвох.** Шаблон `"/users/"` (с завершающим слэшем, без метода) в старом
стиле — это префиксный матч, который перехватит `/users/1/orders/5`. Новый
`"GET /users/{id}"` матчит ровно один сегмент, если явно не указано
`{id...}`.

---

## Почему `http.Server` без настроенных таймаутов считается уязвимостью?

**Коротко.** У `http.Server` по умолчанию **нет** ограничений на время чтения
заголовков, чтения тела, записи ответа и жизни простаивающего соединения — это
классическая уязвимость к атаке Slowloris: клиент открывает много соединений и
шлёт байты по одному в час, удерживая горутины и файловые дескрипторы сервера
занятыми.

```go
srv := &http.Server{
    Addr:              ":8080",
    Handler:           mux,
    ReadHeaderTimeout: 5 * time.Second,
    ReadTimeout:       10 * time.Second,
    WriteTimeout:      10 * time.Second,
    IdleTimeout:       120 * time.Second,
    MaxHeaderBytes:    1 << 20, // 1 МиБ
}
```

`ReadHeaderTimeout` — минимально обязательный из всех: он один закрывает
основной вектор Slowloris (медленная отправка заголовков) и почти никогда не
мешает нормальным клиентам. `WriteTimeout` стоит выставлять осторожнее — если
хендлер стримит большой ответ дольше таймаута, сервер оборвёт соединение
посередине.

**Подвох.** «Достаточно `WriteTimeout`, он же покрывает весь запрос?» Нет —
`WriteTimeout` отсчитывается с момента, когда сервер начал читать заголовки
запроса, до конца записи ответа; он не защищает по отдельности медленное
чтение тела запроса от медленной записи ответа. Для тонкого контроля таймаута
именно на этот конкретный запрос (например, разное время для разных ручек)
используют `http.ResponseController` (Go 1.20+) прямо внутри хендлера.

---

## Как правильно останавливать HTTP-сервер (graceful shutdown)?

**Коротко.** `srv.Shutdown(ctx)` — «вежливая» остановка: сервер перестаёт
принимать новые соединения, но даёт уже начатым запросам доработать (пока не
истечёт переданный `ctx` или клиент не отключится). `srv.Close()` — резкая:
рвёт все соединения немедленно.

```go
func run() error {
    srv := &http.Server{Addr: ":8080", Handler: mux}

    ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
    defer stop()

    errCh := make(chan error, 1)
    go func() {
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            errCh <- err
        }
    }()

    select {
    case err := <-errCh:
        return err
    case <-ctx.Done():
    }

    shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()
    return srv.Shutdown(shutdownCtx)
}
```

`signal.NotifyContext` отменяет контекст при получении сигнала — удобнее
ручной работы с `signal.Notify` и каналом. `ListenAndServe` при штатной
остановке через `Shutdown` всегда возвращает именно `http.ErrServerClosed`, а
не `nil` — это ожидаемое значение, а не ошибка запуска.

**Подвох.** Если у долгоживущих соединений (WebSocket, SSE, long-polling) нет
собственного механизма завершения, `Shutdown` будет ждать их до истечения
переданного `ctx`, а по истечении — вернёт ошибку контекста, но сами
соединения при этом всё равно останутся не закрытыми до следующего шага;
хендлеры таких соединений обязаны сами слушать `r.Context().Done()`
(отменяется при остановке сервера) и завершаться.

---

## Почему `http.DefaultClient` — плохая идея в проде, и как настроить свой?

**Коротко.** У `http.DefaultClient` (как и у пакетных функций `http.Get`/
`http.Post`, которые его используют) нет таймаута вообще — зависший сервер на
другом конце способен подвесить запрос навсегда. В продовом коде всегда
заводят собственный `http.Client` с явным `Timeout` и настроенным
`Transport`.

```go
client := &http.Client{
    Timeout: 10 * time.Second,
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 20,
        IdleConnTimeout:     90 * time.Second,
    },
}
```

`http.Client` потокобезопасен и рассчитан на переиспользование — создавать
новый клиент на каждый запрос значит терять пул соединений `Transport`
(keep-alive) и заново делать TCP+TLS handshake каждый раз.

После каждого запроса тело ответа нужно не только закрыть, но и дочитать до
конца — иначе `Transport` не сможет вернуть TCP-соединение в пул для
переиспользования:

```go
resp, err := client.Do(req)
if err != nil {
    return err
}
defer resp.Body.Close()

// если тело не нужно целиком (например, при ошибке) —
// дочитать и выбросить, чтобы соединение ушло обратно в пул
defer io.Copy(io.Discard, resp.Body)

body, err := io.ReadAll(resp.Body)
```

**Подвох.** «Я закрыл `resp.Body`, значит соединение точно освободится?»
`Close()` без предварительного полного чтения тела заставляет `Transport`
считать соединение «грязным» и просто закрыть TCP-сокет вместо возврата в
пул keep-alive — работать это будет, но каждый следующий запрос снова
устанавливает новое соединение, что медленнее и держит больше файловых
дескрипторов открытыми, чем нужно.

**Глубже.** Мокать HTTP-клиент в тестах принято не через интерфейсы поверх
`http.Client` (что на практике избыточно), а через подмену `Transport` —
достаточно реализовать интерфейс `http.RoundTripper` с одним методом
`RoundTrip(*http.Request) (*http.Response, error)`.

---

## Как тестировать HTTP-хендлеры и клиентов?

**Коротко.** Для хендлеров — `httptest.NewRecorder()`, который реализует
`http.ResponseWriter` в памяти, без реального сетевого сокета. Для клиентов,
которым нужен настоящий сервер, — `httptest.NewServer`, поднимающий
`net/http` на случайном локальном порту.

```go
func TestHandler(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/users/42", nil)
    req.SetPathValue("id", "42") // go 1.22+: подстановка PathValue напрямую в тесте
    rec := httptest.NewRecorder()

    getUser(rec, req)

    if rec.Code != http.StatusOK {
        t.Fatalf("got status %d, want %d", rec.Code, http.StatusOK)
    }
}

func TestClient(t *testing.T) {
    ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusCreated)
    }))
    defer ts.Close()

    resp, err := ts.Client().Post(ts.URL, "application/json", strings.NewReader(`{}`))
    if err != nil {
        t.Fatal(err)
    }
    defer resp.Body.Close()
    if resp.StatusCode != http.StatusCreated {
        t.Fatalf("got %d", resp.StatusCode)
    }
}
```

**Подвох.** `w.WriteHeader` можно вызвать ровно один раз, и только до первой
записи тела — первый же `w.Write` неявно шлёт `200 OK`, если `WriteHeader` ещё
не вызывался. Если код пытается отдать ошибку после того, как в тело уже
что-то записали, статус ответа изменить уже нельзя: заголовки к тому моменту
физически ушли клиенту. Отсюда правило — сначала полностью подготовить и
провалидировать ответ, и только потом писать в `http.ResponseWriter`.

---

[← Стандартная библиотека](stdlib-essentials.md) · [🏠 Домой](../README.md) · [Идиомы, стиль и архитектура →](idioms-style.md)
