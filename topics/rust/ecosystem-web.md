# Rust: экосистема и типовой бэкенд-сервис

[🏠 Карта тем по Rust](README.md)

## Что нужно знать

- **Стандартная библиотека намеренно маленькая**: нет HTTP, нет JSON, нет
  генератора случайных чисел, нет async-рантайма, нет дат сверх
  `SystemTime`/`Instant`. Всё это — крейты, и знание «канонического набора»
  на собеседовании проверяют почти всегда.
- **Базовый набор**: `serde` + `serde_json` (сериализация через derive),
  `tokio` (рантайм), `reqwest` (HTTP-клиент), `axum` или `actix-web`
  (сервер), `sqlx` / `diesel` / `sea-orm` (БД), `tracing` +
  `tracing-subscriber` (структурные логи и спаны), `thiserror`/`anyhow`
  (ошибки), `clap` (CLI), `config`/`figment` (конфигурация), `chrono` или
  `time` (даты), `uuid`, `regex`, `rand`, `itertools`.
- **`serde`**: `#[derive(Serialize, Deserialize)]`, атрибуты `rename`,
  `rename_all`, `default`, `skip_serializing_if`, `flatten`, `tag` для
  внешне/внутренне размеченных enum. Ошибки десериализации — обычный
  `Result`, а не исключение.
- **`axum`**: обработчик — обычная `async fn`, аргументы извлекаются
  типами-экстракторами (`Json<T>`, `Path<T>`, `Query<T>`, `State<S>`), ответ
  — всё, что реализует `IntoResponse`. Мидлвари — из `tower`
  (таймауты, ограничение параллелизма, трассировка), тот же слой переиспользуют
  клиенты.
- **`sqlx`** проверяет SQL на этапе компиляции по живой схеме
  (`query!`-макрос) и не является ORM; `diesel` — типизированный DSL,
  `sea-orm` — ближе к классическому ORM. Разница «проверка SQL против
  абстракции над SQL» — хороший ответ на вопрос о выборе.
- **Наблюдаемость**: `tracing` даёт спаны и структурные поля, экспорт —
  `tracing-opentelemetry`, метрики — `metrics` или `prometheus`.
- **Типичная архитектура сервиса**: `main` собирает конфиг, пул БД,
  состояние `AppState`, роутер и запускает `tokio`; доменный слой не знает о
  HTTP и БД; ошибки домена превращаются в HTTP-ответ реализацией
  `IntoResponse`. Языконезависимая часть — в
  [архитектуре](../../fundamentals/architecture.md).
- **Где Rust реально применяют**: сетевые прокси и балансировщики, БД и
  движки хранения, обработка данных, CLI-утилиты, WebAssembly, embedded,
  расширения для Python (`pyo3`) и Node (`napi-rs`), инфраструктурные
  компоненты внутри Go/Java-стека.
- **Что спрашивают**: как выбрать между `axum` и `actix-web`; почему в
  Rust нет одного «Django» (компоненты собирают из крейтов); как
  организовать graceful shutdown (сигнал → `tokio::select!` →
  `axum::serve(...).with_graceful_shutdown(...)`).

## Ссылки

- [crates.io](https://crates.io/) и [lib.rs](https://lib.rs/) — поиск и сравнение крейтов по популярности.
- [serde](https://serde.rs/) — руководство по атрибутам и моделям данных.
- [axum](https://docs.rs/axum) и [tower](https://docs.rs/tower) — сервер и слой мидлварей.
- [sqlx](https://docs.rs/sqlx) — проверка SQL на этапе компиляции.
- [tracing](https://docs.rs/tracing) — структурная трассировка.
- [Zero To Production In Rust](https://www.zero2prod.com/) — сквозной пример боевого сервиса.
