# Rust: инструменты, сборка, профилирование

[🏠 Карта тем по Rust](README.md)

## Что нужно знать

- **`rustup`** — менеджер тулчейнов: каналы `stable`/`beta`/`nightly`,
  `rustup component add clippy rustfmt`, `rustup target add` для
  кросс-компиляции, `rust-toolchain.toml` фиксирует версию для проекта.
  Релизы стабильного канала выходят каждые шесть недель.
- **`cargo clippy`** — более 700 линтов, включая идиоматические
  (`clippy::needless_clone`, `redundant_closure`, `large_enum_variant`);
  в CI гоняют с `-D warnings`. **`cargo fmt`** — единый стиль, спорить не о
  чем, как и в Go.
- **`rust-analyzer`** — LSP-сервер, фактический стандарт для IDE.
- **Профили сборки**: `dev` (без оптимизаций, с отладкой, переполнение —
  паника) и `release` (`opt-level = 3`, переполнение оборачивается).
  Тюнинг: `lto = "thin"/"fat"`, `codegen-units = 1`, `panic = "abort"`,
  `strip = true`, `debug = true` для профилирования релиза.
- **Ускорение компиляции**: `cargo check` вместо `build`, разбиение на
  крейты, `sccache`, альтернативный линкер (`lld`, `mold`),
  `cargo build --timings` для поиска узкого места.
- **Профилирование**: `perf` + `flamegraph` (`cargo flamegraph`),
  `samply`, Instruments/VTune; аллокации — `dhat`, `heaptrack`,
  `jemalloc`-статистика; `cargo bloat` — что занимает место в бинарнике.
- **Безопасность цепочки поставок**: `cargo audit` (уязвимости из
  RustSec), `cargo deny` (лицензии, дубликаты версий, запрещённые крейты),
  `cargo vet`, `cargo geiger` (сколько `unsafe` в зависимостях).
- **Полезные подкоманды**: `cargo tree -d` (дубликаты версий),
  `cargo expand`, `cargo udeps` (лишние зависимости), `cargo watch`,
  `cargo doc --open`, `cargo publish` для crates.io.
- **Кросс-компиляция и деплой**: `--target`, `cross` (сборка в докере),
  статическая линковка через `x86_64-unknown-linux-musl`, многоступенчатые
  Dockerfile с кешированием `cargo chef`.
- **Диагностика в рантайме**: `RUST_BACKTRACE=1`, `RUST_LOG` + `tracing`/
  `env_logger`, `debug_assertions`.
- **Что спрашивают**: почему Rust долго компилируется (мономорфизация,
  LLVM, крейт как единица компиляции) и как это лечат; чем `cargo check`
  отличается от `build`; зачем `codegen-units = 1`.

## Ссылки

- [The Cargo Book: Profiles](https://doc.rust-lang.org/cargo/reference/profiles.html) — все параметры сборки.
- [The Rust Performance Book](https://nnethercote.github.io/perf-book/) — практическое руководство по ускорению кода и сборки.
- [Clippy lints](https://rust-lang.github.io/rust-clippy/master/) — каталог линтов с объяснениями.
- [rustup book](https://rust-lang.github.io/rustup/) — тулчейны, компоненты, таргеты.
- [cargo-audit / RustSec](https://rustsec.org/) — база уязвимостей крейтов.
- [Flamegraph для Rust](https://github.com/flamegraph-rs/flamegraph) — профилирование в одну команду.
