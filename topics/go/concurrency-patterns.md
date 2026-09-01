# Go: паттерны конкурентности

[🏠 Карта тем по Go](README.md)

## Что нужно знать

- **Worker pool**: N горутин читают из общего входного канала, пишут в
  выходной; количество воркеров ограничивает параллелизм и потребление
  ресурсов. Вопрос «сколько воркеров» — ответ зависит от природы нагрузки:
  CPU-bound ≈ `GOMAXPROCS`, I/O-bound — сильно больше.
- **Семафор** для ограничения параллелизма без пула: буферизованный канал
  `sem := make(chan struct{}, n)` или `golang.org/x/sync/semaphore`.
- **Fan-out / fan-in**: раздать работу нескольким горутинам и собрать
  результаты в один канал; для fan-in нужна `WaitGroup` и закрытие выходного
  канала после `Wait()`.
- **Pipeline**: цепочка стадий, каждая — горутина, читающая из входного канала
  и пишущая в выходной. Ключевое правило — **каждая стадия должна корректно
  завершаться при отмене**, иначе течут горутины (`done`-канал или `ctx`).
- **`errgroup`** (`golang.org/x/sync/errgroup`) — практический стандарт:
  `g, ctx := errgroup.WithContext(ctx)`, `g.Go(func() error {...})`,
  `g.Wait()` возвращает первую ошибку и отменяет общий контекст;
  `g.SetLimit(n)` ограничивает параллелизм.
- **Отмена и graceful shutdown**: `signal.NotifyContext`, закрытие приёма
  новых задач, дренаж очереди, `server.Shutdown(ctx)` с таймаутом.
- **Утечки горутин** — главная тема практических вопросов. Правила:
  у каждой запущенной горутины должен быть определён момент завершения; тот,
  кто запускает, отвечает за остановку; никогда не отправляйте в канал без
  `select` с `ctx.Done()`.
- **Rate limiting**: `time.Ticker`, `golang.org/x/time/rate` (token bucket),
  разница между ограничением RPS и ограничением параллелизма.
- **Publish/subscribe и broadcast**: `close(done)` как broadcast, либо список
  подписчиков под мьютексом.
- **Singleflight** (`golang.org/x/sync/singleflight`) — схлопывание
  одновременных одинаковых запросов, защита от cache stampede.
- **Идемпотентность и порядок**: результаты из пула приходят в произвольном
  порядке; если порядок важен — индексируйте задачи и собирайте в слайс по
  индексу, а не по времени прихода.
- **`for-select` идиома** и вложенный `select` с `default` для неблокирующей
  отправки — уметь написать на доске.

## Ссылки

- [Go Concurrency Patterns: Pipelines and cancellation](https://go.dev/blog/pipelines) — эталонная статья про пайплайны, fan-in/fan-out и корректную отмену.
- [Advanced Go Concurrency Patterns — Sameer Ajmani](https://go.dev/blog/io2013-talk-concurrency) — более сложные комбинации select, таймеров и состояния.
- [pkg.go.dev/golang.org/x/sync/errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup) — группа горутин с ошибкой, контекстом и лимитом.
- [pkg.go.dev/golang.org/x/sync/singleflight](https://pkg.go.dev/golang.org/x/sync/singleflight) — схлопывание дублирующихся вызовов.
- [pkg.go.dev/golang.org/x/time/rate](https://pkg.go.dev/golang.org/x/time/rate) — token bucket для ограничения скорости.
- [Concurrency in Go — книга Katherine Cox-Buday](https://www.oreilly.com/library/view/concurrency-in-go/9781491941294/) — систематический разбор всех паттернов с примерами.
