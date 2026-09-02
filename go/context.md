# context.Context

[← sync, atomic и модель памяти](sync-atomic.md) · [🏠 Домой](../README.md) · [Паттерны конкурентности →](concurrency-patterns.md)

---

## Зачем нужен `context.Context` и почему отмена родителя отменяет всех потомков?

**Коротко.** `context.Context` — это сквозной механизм отмены, дедлайнов и
передачи request-scoped значений через границы горутин и вызовов API.
Контексты образуют **дерево**: у каждого дочернего контекста есть родитель,
и отмена родителя рекурсивно отменяет всё поддерево.

```go
func main() {
	parent, cancelParent := context.WithCancel(context.Background())
	child, cancelChild := context.WithTimeout(parent, time.Second)
	defer cancelChild()

	cancelParent() // отмена родителя отменяет всё поддерево, включая child

	<-child.Done()
	fmt.Println(child.Err()) // context canceled — причина пришла от родителя, не от таймаута
}
```

**Подвох.** Дочерний контекст может **сократить** дедлайн родителя, но
никогда не может его продлить — если у родителя `WithTimeout(1s)`, а у
потомка `WithTimeout(10s)`, реальный дедлайн потомка всё равно ограничен
одной секундой родителя.

---

## Какие есть конструкторы `context` и когда каким пользоваться?

**Коротко.** `context.Background()` — корень дерева контекстов, используется
в `main`, при инициализации и в тестах. `context.TODO()` — временная заглушка
на то место, где контекст ещё не протянут по цепочке вызовов, но должен быть.
Остальные — `WithCancel`, `WithTimeout`, `WithDeadline`, `WithValue` —
оборачивают родителя, добавляя одно новое свойство.

```go
// go 1.20+
func main() {
	ctx, cancel := context.WithCancelCause(context.Background())
	go func() {
		time.Sleep(10 * time.Millisecond)
		cancel(fmt.Errorf("worker gave up")) // явная причина отмены, не просто "canceled"
	}()

	<-ctx.Done()
	fmt.Println(ctx.Err())          // context canceled
	fmt.Println(context.Cause(ctx)) // worker gave up
}
```

С Go 1.21 добавились `context.WithoutCancel` (получить контекст, который
наследует значения, но не отмену родителя — полезно для фоновых операций,
которые обязаны пережить сам запрос) и `context.AfterFunc` (зарегистрировать
колбэк на момент отмены контекста, не заводя отдельную горутину с `select`
вручную).

**Подвох.** `context.TODO()` — не "контекст на будущее", это явный маркер
технического долга: если он остался в коде после рефакторинга, значит,
кто-то не довёл протягивание контекста до конца.

---

## Почему `cancel()` нужно вызывать всегда, даже если контекст истёк сам?

**Коротко.** `WithCancel`/`WithTimeout`/`WithDeadline` заводят внутренний
таймер и горутину-наблюдателя за родителем. Если не вызвать `cancel()`
явно, эти ресурсы освободятся только когда родительский контекст тоже будет
отменён (а если родитель — `Background()`, то никогда). Идиома —
`defer cancel()` сразу после создания.

```go
func doRequest() error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel() // без этого таймер и горутина живут лишние секунды даже после успешного ответа
	return callAPI(ctx)
}
```

**Подвох.** `go vet` умеет ловить забытый `cancel()` правилом `lostcancel` —
но только когда потеря видна статически (например, переменная `cancel`
нигде не используется). Если `cancel` передаётся дальше и теряется в
условной ветке, статический анализ уже не поможет — только код-ревью.

---

## Как правильно передавать `context.Context` в функции, и почему его не хранят в структуре?

**Коротко.** `ctx` — всегда **первый параметр** функции, называется именно
`ctx`, никогда не бывает `nil` и почти никогда не хранится в полях структуры.
Причина — контекст живёт ровно столько, сколько живёт конкретный вызов или
запрос; сохранённый в структуре контекст рискует пережить своё "время жизни"
и незаметно использоваться в чужом, уже неактуальном запросе.

```go
// ХОРОШО: ctx явно передаётся в каждый вызов
func FetchUser(ctx context.Context, id int) (*User, error) {
	row := db.QueryRowContext(ctx, "SELECT name FROM users WHERE id = $1", id)
	var name string
	if err := row.Scan(&name); err != nil {
		return nil, err
	}
	return &User{ID: id, Name: name}, nil
}

// ПЛОХО: контекст "протухает", но по сигнатуре методов Service это не видно
type Service struct {
	ctx context.Context
}
```

**Подвох.** Исключения из правила "не хранить в структуре" редки и
осознанны — например, `http.Request.ctx` в стандартной библиотеке хранится
именно так, но это внутренняя деталь реализации `net/http`, а не образец
для прикладного кода.

---

## Для чего нужен `context.WithValue`, и почему им нельзя передавать параметры функций?

**Коротко.** `WithValue` предназначен исключительно для **request-scoped**
данных, которые нужны на всех уровнях вызовов, но неудобно протаскивать
явными параметрами: trace id, идентификатор пользователя, логгер запроса.
Это не механизм передачи обычных параметров или зависимостей — для них
сигнатура функции нагляднее и безопаснее по типам.

```go
type ctxKey int

const requestIDKey ctxKey = 0 // неэкспортируемый собственный тип ключа — не int, не string

func withRequestID(ctx context.Context, id string) context.Context {
	return context.WithValue(ctx, requestIDKey, id)
}

func requestID(ctx context.Context) (string, bool) {
	id, ok := ctx.Value(requestIDKey).(string)
	return id, ok
}
```

**Подвох.** Ключ обязан быть собственным неэкспортируемым типом (`ctxKey`,
а не голый `string` или `int`) — иначе два разных пакета, использующих
одинаковую строку в качестве ключа, тихо затрут значения друг друга. Ещё
одна деталь для дотошных: поиск значения по цепочке `WithValue` — линейный
проход по каждому уровню обёртки, так что десятки вложенных `WithValue`
на одном запросе — уже не бесплатная операция.

---

## Как `context` интегрируется со стандартной библиотекой?

**Коротко.** Отмена и дедлайны из `context` пронизывают ключевые пакеты
`net/http`, `database/sql` и `os/exec` — не нужно изобретать свою обёртку
поверх таймеров, достаточно передать контекст туда, где библиотека этого
явно ждёт.

```go
func handler(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context() // отменяется автоматически, если клиент разорвёт соединение
	row := db.QueryRowContext(ctx, "SELECT name FROM users WHERE id = $1", 1)
	var name string
	if err := row.Scan(&name); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	fmt.Fprintln(w, name)
}

func runGit(ctx context.Context, dir string) error {
	cmd := exec.CommandContext(ctx, "git", "status")
	cmd.Dir = dir
	return cmd.Run() // процесс будет убит, если ctx отменится до завершения
}
```

**Глубже.** Типичные практические ошибки с контекстом: передать
`context.Background()` внутрь HTTP-хендлера вместо `r.Context()` (тогда
отмена запроса клиентом не остановит работу на сервере); сохранить `ctx` в
поле структуры и переиспользовать его после того, как он уже отменён;
запустить дорогую операцию, не проверив `ctx.Err()` заранее, хотя было уже
очевидно, что дедлайн истёк.

---

[← sync, atomic и модель памяти](sync-atomic.md) · [🏠 Домой](../README.md) · [Паттерны конкурентности →](concurrency-patterns.md)
