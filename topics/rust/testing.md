# Rust: тестирование

[🏠 Карта тем по Rust](README.md)

## Что нужно знать

- **Тесты — часть языка**: `#[test]` на функции, `cargo test`. Юнит-тесты
  живут рядом с кодом в `mod tests` под `#[cfg(test)]` (имеют доступ к
  приватным элементам), интеграционные — в каталоге `tests/` (видят только
  публичный API, каждый файл — отдельный крейт).
- **Ассерты**: `assert!`, `assert_eq!`, `assert_ne!` (требуют `Debug`),
  `#[should_panic(expected = "...")]`, тесты, возвращающие
  `Result<(), E>` (можно писать `?`), `#[ignore]` для долгих.
- **Doc-тесты** — примеры в `///`-комментариях компилируются и запускаются
  `cargo test`. Уникальная для Rust вещь: документация не может протухнуть
  незаметно. Скрытые строки настройки помечают `#`, компиляцию без запуска —
  `no_run`, ожидание ошибки компиляции — `compile_fail`.
- **Тесты идут параллельно** в потоках; `--test-threads=1` для
  последовательного запуска, вывод показывается только у упавших
  (`--nocapture`, чтобы видеть всегда).
- **Организация**: `tests/common/mod.rs` для общего кода, `#[cfg(test)]`
  зависимости в `[dev-dependencies]`, фикстуры через обычные функции —
  фреймворка xUnit в стандартной библиотеке нет.
- **Полезные крейты**: `rstest` (параметризованные тесты и фикстуры),
  `proptest`/`quickcheck` (property-based), `insta` (snapshot),
  `mockall` (моки трейтов), `criterion` (бенчмарки со статистикой),
  `wiremock`/`httpmock` (HTTP), `testcontainers` (БД в докере),
  `cargo-nextest` (быстрый раннер), `cargo-llvm-cov`/`tarpaulin` (покрытие).
- **Бенчмарки**: `#[bench]` — только nightly, поэтому на стабильной версии
  берут `criterion` (или `divan`); он сам считает доверительные интервалы и
  сравнивает с предыдущим прогоном.
- **Fuzzing**: `cargo-fuzz` (libFuzzer) и `afl.rs`; для парсеров считается
  стандартом.
- **Тестируемость и архитектура**: раз моки в Rust требуют трейтов, дизайн
  «зависимость как обобщённый параметр или `dyn Trait`» — прямой аналог
  внедрения зависимостей; см.
  [DI в fundamentals](../../fundamentals/dependency-injection.md).
- **Что спрашивают**: чем юнит-тесты отличаются от интеграционных именно в
  Rust (доступ к приватному и границы крейта); как протестировать
  `async`-код (`#[tokio::test]`); как проверить, что код не компилируется
  (`compile_fail` doc-тест или `trybuild`).

## Ссылки

- [Book: Writing Automated Tests](https://doc.rust-lang.org/book/ch11-00-testing.html) — организация тестов и ассерты.
- [Rustdoc Book: Documentation tests](https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html) — правила doc-тестов.
- [criterion](https://bheisler.github.io/criterion.rs/book/) — бенчмарки на стабильном компиляторе.
- [proptest](https://proptest-rs.github.io/proptest/) — property-based тестирование.
- [cargo-nextest](https://nexte.st/) — альтернативный раннер тестов.
