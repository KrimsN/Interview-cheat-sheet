# Rust: модули, крейты, Cargo

[🏠 Карта тем по Rust](README.md)

## Что нужно знать

- **Иерархия**: пакет (`Cargo.toml`) → крейт (единица компиляции: библиотека
  `src/lib.rs` и/или бинарники `src/main.rs`, `src/bin/*.rs`) → модули
  (`mod`) → элементы. Один пакет — максимум одна библиотека и сколько угодно
  бинарников.
- **Модули объявляются, а не «находятся»**: `mod foo;` подключает
  `foo.rs` или `foo/mod.rs`. Современный стиль — `foo.rs` + каталог `foo/`.
- **Видимость по умолчанию приватная**, наружу — `pub`. Уровни:
  `pub(crate)`, `pub(super)`, `pub(in path)`. Приватное видно потомкам
  модуля, но не соседям — обратная логика по сравнению с Java.
- **Пути**: `crate::`, `self::`, `super::`, абсолютные пути к внешним крейтам
  по имени; `use ... as ...`, `pub use` — реэкспорт (основной инструмент
  «фасада»: внутренняя раскладка модулей не становится публичным API).
- **Прелюдия** подключается автоматически; всё остальное — через `use`.
- **Cargo**: `cargo build/run/test/bench/doc/check/clippy/fmt`,
  `cargo add/remove/update/tree`, профили `[profile.dev]` и
  `[profile.release]`, `Cargo.lock` (коммитится для бинарников; для библиотек
  раньше не коммитили, сейчас обычно тоже коммитят ради воспроизводимости CI).
- **Версионирование**: SemVer, «карет»-требование `1.2.3` означает
  совместимость по мажорной версии. В отличие от Go с его MVS, Cargo
  выбирает **максимальную** совместимую версию, но допускает несколько
  мажорных версий одного крейта в графе.
- **Features** — условная компиляция и опциональные зависимости; они
  **аддитивны** (объединяются по всему графу), поэтому нельзя делать
  «взаимоисключающие» флаги. `default-features = false` — как отключают
  тяжёлые куски. `no_std` — сборка без стандартной библиотеки.
- **Workspace**: общий `Cargo.lock` и `target/`, единый набор версий;
  типичная раскладка для сервиса из нескольких крейтов.
- **`build.rs`** — скрипт сборки (кодогенерация, линковка с C),
  `[build-dependencies]`.
- **Условная компиляция**: `#[cfg(test)]`, `#[cfg(feature = "x")]`,
  `#[cfg(target_os = "linux")]`, `cfg!(...)` в выражении.
- **Что спрашивают**: чем крейт отличается от пакета и модуля; что такое
  orphan rule в терминах крейтов; зачем `pub use`; почему две версии одного
  крейта в графе приводят к ошибке «expected struct `X`, found struct `X`».

## Ссылки

- [Book: Managing Growing Projects](https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html) — пакеты, крейты, модули, пути.
- [The Cargo Book](https://doc.rust-lang.org/cargo/) — манифест, профили, workspace.
- [Cargo Book: Features](https://doc.rust-lang.org/cargo/reference/features.html) — аддитивность и опциональные зависимости.
- [Cargo Book: SemVer compatibility](https://doc.rust-lang.org/cargo/reference/semver.html) — что считается ломающим изменением.
- [Rust Reference: Conditional compilation](https://doc.rust-lang.org/reference/conditional-compilation.html) — все формы `cfg`.
