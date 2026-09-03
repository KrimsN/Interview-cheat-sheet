# Тестирование

[← async/await, Future и Tokio](async-await.md) · [🏠 Домой](../README.md) · [Инструменты, сборка, профилирование →](tooling.md)

---

## Чем юнит-тесты отличаются от интеграционных именно в Rust?

**Коротко.** Юнит-тесты живут рядом с кодом в модуле `#[cfg(test)] mod tests`
и **видят приватные элементы**. Интеграционные лежат в каталоге `tests/`,
каждый файл — отдельный крейт, и им доступен только публичный API.

```rust
// src/lib.rs
pub fn public_add(a: i32, b: i32) -> i32 { internal(a, b) }

fn internal(a: i32, b: i32) -> i32 { a + b }

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn internal_works() {
        assert_eq!(internal(2, 2), 4);   // приватная функция доступна
    }
}
```

```rust
// tests/api.rs — отдельный крейт, видит только pub
use my_crate::public_add;

#[test]
fn public_api_works() {
    assert_eq!(public_add(2, 40), 42);
}
```

Практический вывод: интеграционные тесты — это ещё и проверка того, что
публичный API вообще пригоден к использованию. Если тест в `tests/` написать
неудобно, пользователю библиотеки будет так же неудобно.

**Подвох.** Каталог `tests/` работает только для крейта-библиотеки: у
бинарника нет публичного API, который можно импортировать. Отсюда типовая
раскладка «тонкий `main.rs` + вся логика в `lib.rs`».

---

## Как писать тесты и какие есть ассерты?

**Коротко.** `#[test]` на функции, `assert!`/`assert_eq!`/`assert_ne!`
(требуют `Debug` у значений), `#[should_panic]` для проверки паники, тесты,
возвращающие `Result`, чтобы внутри работал `?`.

```rust
fn div(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 { return Err("деление на ноль".into()); }
    Ok(a / b)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn divides() -> Result<(), String> {
        assert_eq!(div(10, 2)?, 5);      // ? работает: тест возвращает Result
        Ok(())
    }

    #[test]
    fn reports_zero() {
        let err = div(1, 0).unwrap_err();
        assert!(err.contains("ноль"), "неожиданное сообщение: {err}");
    }

    #[test]
    #[should_panic(expected = "index out of bounds")]
    fn panics_on_bad_index() {
        let v: Vec<i32> = vec![];
        let _ = v[0];
    }

    #[test]
    #[ignore = "долгий, запускать вручную"]
    fn slow() { /* cargo test -- --ignored */ }
}
```

Запуск: `cargo test`, конкретный тест — `cargo test divides`, только
проигнорированные — `cargo test -- --ignored`.

**Подвох.** Тесты выполняются **параллельно**, каждый в своём потоке. Тесты,
которые пишут в один файл, слушают один порт или трогают глобальное
состояние, будут флакать. Лечится изоляцией (временные каталоги, порт `0`) или
`cargo test -- --test-threads=1`.

---

## Что такое doc-тесты и почему это важно?

**Коротко.** Примеры кода в `///`-комментариях компилируются и запускаются
`cargo test`. Документация физически не может протухнуть незаметно — такого
из коробки нет почти нигде.

````rust
/// Складывает два числа.
///
/// # Примеры
///
/// ```
/// use my_crate::add;
/// assert_eq!(add(2, 40), 42);
/// ```
///
/// Ошибочный ввод приводит к панике:
///
/// ```should_panic
/// my_crate::add_positive(0, 1);
/// ```
pub fn add(a: i32, b: i32) -> i32 { a + b }
````

Модификаторы блока: `ignore` (не компилировать), `no_run` (собрать, но не
запускать — для сетевых примеров), `should_panic`, `compile_fail` (пример
**обязан** не компилироваться — так проверяют, что API запрещает
неправильное использование), а строки, начинающиеся с `#`, скрываются из
рендера, но участвуют в компиляции.

**Глубже.** `compile_fail` — способ протестировать сами гарантии типов:
например, что `Handle` нельзя отправить в другой поток. Для более сложных
проверок такого рода берут крейт `trybuild`.

---

## Как тестировать асинхронный код?

**Коротко.** `#[tokio::test]` вместо `#[test]` — макрос сам создаёт рантайм.
Время в тестах контролируют «паузой» таймера, чтобы не спать по-настоящему.

```rust
#[tokio::test]
async fn fetches() {
    let result = fetch_user(1).await;
    assert!(result.is_ok());
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn parallel() { /* ... */ }

#[tokio::test(start_paused = true)]
async fn timeouts_without_waiting() {
    // таймер виртуальный: sleep завершится мгновенно, но логика таймаутов проверится
    tokio::time::sleep(std::time::Duration::from_secs(3600)).await;
}
```

Для HTTP-зависимостей поднимают заглушку (`wiremock`, `httpmock`), для базы —
`testcontainers` (реальный PostgreSQL в Docker) либо транзакцию с откатом
после теста.

---

## Какие крейты для тестирования стоит знать?

**Коротко.** Стандартной библиотеке хватает `#[test]`; всё остальное — из
экосистемы.

| Крейт | Зачем |
|---|---|
| `rstest` | параметризованные тесты и фикстуры |
| `proptest`, `quickcheck` | property-based тестирование |
| `insta` | snapshot-тесты, ревью изменений вывода |
| `mockall` | моки трейтов |
| `criterion`, `divan` | бенчмарки со статистикой |
| `wiremock`, `httpmock` | заглушки HTTP |
| `testcontainers` | реальная БД в Docker на время тестов |
| `cargo-nextest` | быстрый параллельный раннер |
| `cargo-llvm-cov` | покрытие кода |

```rust
// property-based: свойство вместо примеров
proptest::proptest! {
    #[test]
    fn roundtrip(s: String) {
        let encoded = encode(&s);
        proptest::prop_assert_eq!(decode(&encoded).unwrap(), s);
    }
}
```

Property-based тесты особенно уместны для парсеров, сериализации и любых пар
«кодировать/декодировать»: они сами ищут минимальный контрпример.

**Глубже.** Фреймворка вроде xUnit с `setUp`/`tearDown` в Rust нет. Фикстуры —
обычные функции, а очистка — RAII: объект, создающий временный каталог,
удаляет его в `Drop`. Это ещё одно применение [владения](ownership.md).

---

## Как измерять производительность в тестах?

**Коротко.** `#[bench]` доступен только на nightly, поэтому на стабильной
версии используют `criterion` — он считает доверительные интервалы и
сравнивает прогон с предыдущим.

```rust
// benches/my_bench.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn fib(n: u64) -> u64 { if n < 2 { n } else { fib(n - 1) + fib(n - 2) } }

fn bench(c: &mut Criterion) {
    c.bench_function("fib 20", |b| b.iter(|| fib(black_box(20))));
}

criterion_group!(benches, bench);
criterion_main!(benches);
```

```bash
cargo bench
```

`black_box` не даёт компилятору выкинуть вычисление как бесполезное — без
него бенчмарк часто измеряет пустой цикл. Это классический вопрос «почему
ваш бенчмарк показывает 0 нс».

---

## Как тестировать код с зависимостями?

**Коротко.** Зависимость объявляют трейтом, а в тест подставляют другую
реализацию — через обобщённый параметр (статически) или `Box<dyn Trait>`
(динамически). Это ровно внедрение зависимостей, без контейнеров и
фреймворков.

```rust
trait Clock {
    fn now(&self) -> u64;
}

struct SystemClock;
impl Clock for SystemClock {
    fn now(&self) -> u64 {
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH).unwrap().as_secs()
    }
}

struct FixedClock(u64);
impl Clock for FixedClock { fn now(&self) -> u64 { self.0 } }

fn is_expired(c: &impl Clock, deadline: u64) -> bool { c.now() > deadline }

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn detects_expiry() {
        assert!(is_expired(&FixedClock(100), 50));
        assert!(!is_expired(&FixedClock(10), 50));
    }
}
```

Общая теория — в [DI из fundamentals](../fundamentals/dependency-injection.md).
Для трейтов с большим числом методов ручные заглушки заменяет `mockall`,
генерирующий мок по `#[automock]`.

---

## Что ещё спрашивают про тесты?

- **Как проверить, что код НЕ компилируется?** `compile_fail` doc-тест или
  `trybuild`.
- **Фаззинг**: `cargo-fuzz` (libFuzzer) и `afl.rs` — для парсеров и всего,
  что читает недоверенный ввод, это фактический стандарт.
- **Где хранить общий код тестов?** В `tests/common/mod.rs` — именно
  `mod.rs`, иначе Cargo примет файл за отдельный тестовый крейт и запустит
  его как тест.
- **Почему тесты не печатают вывод?** `cargo test` перехватывает stdout
  успешных тестов; вернуть — `cargo test -- --nocapture`.

---

[← async/await, Future и Tokio](async-await.md) · [🏠 Домой](../README.md) · [Инструменты, сборка, профилирование →](tooling.md)
