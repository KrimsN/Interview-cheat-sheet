# Экосистема и типовой бэкенд-сервис

[← Производительность и работа с памятью](performance.md) · [🏠 Домой](../README.md) · [Идиомы и проектирование API →](idioms-api-design.md)

---

## Почему в Rust нет «одного Django» и что тогда есть?

**Коротко.** Стандартная библиотека намеренно маленькая: в ней нет HTTP,
JSON, генератора случайных чисел, async-рантайма и работы с датами сверх
`SystemTime`/`Instant`. Сервис собирают из крейтов, и знание канонического
набора проверяют почти на каждом собеседовании.

| Задача | Крейты |
|---|---|
| Сериализация | `serde` + `serde_json` |
| Async-рантайм | `tokio` |
| HTTP-сервер | `axum`, `actix-web` |
| HTTP-клиент | `reqwest` |
| База данных | `sqlx`, `diesel`, `sea-orm` |
| Логи и трассировка | `tracing` + `tracing-subscriber` |
| Ошибки | `thiserror` (библиотека), `anyhow` (приложение) |
| CLI | `clap` |
| Конфигурация | `config`, `figment` |
| Даты | `chrono`, `time` |
| Прочее | `uuid`, `regex`, `rand`, `itertools` |

Причина такого устройства историческая и осознанная: всё, что попало в `std`,
нельзя менять без слома совместимости — а веб-фреймворки и рантаймы за десять
лет менялись радикально. Цена — нужно знать экосистему; выигрыш — `std`
не устарел.

---

## Как работает `serde`?

**Коротко.** `#[derive(Serialize, Deserialize)]` порождает код конвертации на
этапе компиляции — без рефлексии и без затрат в рантайме. Ошибка
десериализации — обычный `Result`, а не исключение.

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct User {
    id: u64,
    full_name: String,
    #[serde(default)]                          // поля может не быть во входе
    active: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    email: Option<String>,
}

fn main() -> Result<(), serde_json::Error> {
    let json = r#"{"id":1,"fullName":"Анна","email":"a@example.com"}"#;
    let u: User = serde_json::from_str(json)?;
    println!("{u:?}");
    // User { id: 1, full_name: "Анна", active: false, email: Some("a@example.com") }

    println!("{}", serde_json::to_string(&u)?);
    // {"id":1,"fullName":"Анна","active":false,"email":"a@example.com"}

    let bad: Result<User, _> = serde_json::from_str(r#"{"id":"нет"}"#);
    println!("{}", bad.is_err());   // true — ошибка как значение
    Ok(())
}
```

Полезные атрибуты: `rename`/`rename_all`, `default`, `skip`,
`skip_serializing_if`, `flatten`, `deny_unknown_fields` и `tag`/`content`
для размеченных enum. Форматов много и они взаимозаменяемы: JSON, YAML, TOML,
MessagePack, CBOR, bincode — один и тот же derive.

---

## Как выглядит сервис на axum?

**Коротко.** Обработчик — обычная `async fn`; аргументы «извлекаются»
типами-экстракторами (`Json<T>`, `Path<T>`, `Query<T>`, `State<S>`), а
результат — всё, что реализует `IntoResponse`.

```rust
use axum::{extract::{Path, State}, http::StatusCode, routing::get, Json, Router};
use serde::Serialize;
use std::sync::Arc;

#[derive(Clone)]
struct AppState { greeting: Arc<String> }

#[derive(Serialize)]
struct User { id: u64, name: String }

async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<u64>,
) -> Result<Json<User>, StatusCode> {
    if id == 0 { return Err(StatusCode::NOT_FOUND); }
    Ok(Json(User { id, name: format!("{} #{id}", state.greeting) }))
}

#[tokio::main]
async fn main() {
    let state = AppState { greeting: Arc::new("пользователь".into()) };
    let app = Router::new()
        .route("/users/{id}", get(get_user))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

Что тут важно для собеседования: экстракторы — это просто трейт
`FromRequestParts`, поэтому свой экстрактор (например, `AuthUser`,
проверяющий токен) пишется в десяток строк и дальше используется как
обычный аргумент. Мидлвари берутся из `tower` — таймауты, ограничение
параллелизма, сжатие, трассировка; тот же слой переиспользуют HTTP-клиенты.

**Подвох.** `axum` против `actix-web`: первый построен на `tower` и
`hyper`, ближе к «просто функции», не требует своего рантайма — сейчас это
выбор по умолчанию. `actix-web` исторически показывает чуть лучшие цифры в
бенчмарках и имеет собственную акторную модель. Оба зрелые; аргументировать
выбор надо интеграцией с остальным стеком, а не таблицами TechEmpower.

---

## Как работают с базой данных?

**Коротко.** `sqlx` — асинхронный драйвер, который **проверяет SQL на этапе
компиляции** по живой схеме, но не является ORM. `diesel` — типизированный
DSL поверх SQL (синхронный). `sea-orm` — ближе к классическому ORM.

```rust
// sqlx: запрос проверяется компилятором по DATABASE_URL
#[derive(sqlx::FromRow)]
struct User { id: i64, name: String }

async fn find(pool: &sqlx::PgPool, id: i64) -> Result<Option<User>, sqlx::Error> {
    sqlx::query_as!(User, "SELECT id, name FROM users WHERE id = $1", id)
        .fetch_optional(pool)
        .await
}
```

Опечатка в имени колонки или несовпадение типов — **ошибка сборки**, а не
падение в рантайме. Для CI без доступа к базе схема кешируется
(`cargo sqlx prepare`).

Хороший ответ на «что выбрать»: `sqlx`, если команда пишет SQL и хочет его
проверку; `diesel`/`sea-orm`, если нужна абстракция над SQL и миграции в
одном флаконе. Языконезависимая часть вопроса — в [разделе про
SQL](../sql/index.md).

---

## Как устроена наблюдаемость?

**Коротко.** `tracing` — структурные логи и спаны (в отличие от `log`, где
только строки). Экспорт в OpenTelemetry — `tracing-opentelemetry`, метрики —
`metrics` или `prometheus`.

```rust
use tracing::{info, instrument};

#[instrument(skip(password))]                 // аргументы попадут в спан, кроме пароля
async fn login(user: &str, password: &str) -> bool {
    info!(attempt = 1, "проверяем учётные данные");
    !password.is_empty() && !user.is_empty()
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt().with_env_filter("info").init();
    println!("{}", login("ann", "secret").await);   // true
}
```

Атрибут `#[instrument]` создаёт спан на всё время выполнения функции —
вложенные логи автоматически получают его поля. Уровни фильтруются через
`RUST_LOG` (`RUST_LOG=my_service=debug,tower_http=info`).

---

## Как выглядит типичная архитектура сервиса?

**Коротко.** `main` собирает конфиг, пул соединений, состояние и роутер и
запускает рантайм; доменный слой ничего не знает про HTTP и БД; ошибки домена
превращаются в HTTP-ответ реализацией `IntoResponse`.

```text
crates/
├── domain/     типы и бизнес-правила, никаких зависимостей от axum и sqlx
├── storage/    репозитории: трейты + реализация на sqlx
└── api/        роутер, экстракторы, преобразование ошибок в HTTP
```

```rust
// превращение доменной ошибки в ответ — граница слоёв
impl axum::response::IntoResponse for DomainError {
    fn into_response(self) -> axum::response::Response {
        let status = match self {
            DomainError::NotFound => axum::http::StatusCode::NOT_FOUND,
            DomainError::Invalid(_) => axum::http::StatusCode::BAD_REQUEST,
            DomainError::Internal(_) => axum::http::StatusCode::INTERNAL_SERVER_ERROR,
        };
        (status, self.to_string()).into_response()
    }
}
```

Разделение на крейты в [workspace](modules-crates.md) даёт больше, чем просто
порядок: Cargo физически запретит циклическую зависимость между слоями, а
сборка станет параллельной. Языконезависимая теория слоёв — в
[архитектуре](../fundamentals/architecture.md).

**Глубже (graceful shutdown).** Стандартный вопрос: как корректно завершить
сервис. Ответ — дождаться сигнала и передать футуру завершения серверу:

```rust
async fn shutdown_signal() {
    tokio::signal::ctrl_c().await.expect("не удалось поставить обработчик");
}

// axum::serve(listener, app).with_graceful_shutdown(shutdown_signal()).await
```

Сервер перестаёт принимать новые соединения и дожидается активных запросов;
дальше закрывают пул БД и сбрасывают буферы трассировки.

---

## Где Rust действительно применяют?

**Коротко.** Там, где важны предсказуемость и цена ошибки: сетевые прокси и
балансировщики, базы данных и движки хранения, обработка данных, CLI-утилиты,
WebAssembly, embedded, расширения для других языков.

Узнаваемые примеры: инфраструктурные компоненты Cloudflare и AWS
(Firecracker), части Android и Windows, движки вроде `ripgrep` и `uv`,
расширения Python на `pyo3` (`polars`, `pydantic-core`), фронтенд-инструменты
на Rust вместо JavaScript.

Типичный сценарий внедрения в компании — **не переписывание всего**, а
точечная замена: горячий сервис или библиотека внутри Go/Java/Python-стека,
подключённая через FFI или как отдельный сервис.

---

[← Производительность и работа с памятью](performance.md) · [🏠 Домой](../README.md) · [Идиомы и проектирование API →](idioms-api-design.md)
