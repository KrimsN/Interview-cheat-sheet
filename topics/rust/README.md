# Rust: карта тем для собеседования

Черновой раздел в формате `topics/`: по каждой теме — краткая выжимка
«что нужно знать» и подборка ссылок (официальная документация в приоритете,
дальше — проверенные разборы). Языконезависимая теория (ООП, SOLID, паттерны,
архитектура, конкурентность как концепция) лежит в
[fundamentals/](../../fundamentals/index.md) — здесь только то, что специфично
для Rust.

## Порядок изучения

### Язык

1. [Базовый синтаксис и модель языка](basics.md) — `let` и иммутабельность,
   выражения, shadowing, editions, cargo с первой минуты.
2. [Владение, перемещение и Drop](ownership.md) — три правила, move-семантика,
   `Copy` против `Clone`, RAII.
3. [Заимствование, ссылки и времена жизни](borrowing-lifetimes.md) —
   «shared XOR mutable», NLL, elision, `'static`, борьба с borrow checker.
4. [Типы, представление в памяти, Sized](types-memory-layout.md) — скаляры,
   переполнение, `repr`, niche-оптимизация, DST и широкие указатели.
5. [Строки, срезы и Cow](strings.md) — `String` против `&str`, UTF-8,
   `OsString`/`CString`, clone-on-write.
6. [Коллекции стандартной библиотеки](collections.md) — `Vec`, `HashMap`,
   entry API, `BTreeMap`, реаллокация и ёмкость.
7. [Перечисления и сопоставление с образцом](enums-pattern-matching.md) —
   типы-суммы, `Option`, исчерпывающий `match`, `let ... else`.
8. [Обработка ошибок](error-handling.md) — `Result`, оператор `?`,
   `thiserror`/`anyhow`, когда уместна паника.
9. [Трейты](traits.md) — явная реализация, orphan rule, ассоциированные типы,
   `dyn` и object safety.
10. [Дженерики и мономорфизация](generics-monomorphization.md) — границы,
    `impl Trait`, const generics, цена статической диспетчеризации.
11. [Замыкания и итераторы](closures-iterators.md) — `Fn`/`FnMut`/`FnOnce`,
    ленивость, адаптеры, `collect`.
12. [Умные указатели и внутренняя изменяемость](smart-pointers.md) — `Box`,
    `Rc`/`Arc`, `RefCell`, `Weak`, `Deref`.
13. [Стандартные трейты и преобразования](std-traits.md) — `From`/`Into`,
    `Display`/`Debug`, `Ord`/`Hash`, `Default`, `AsRef` против `Borrow`.
14. [Модули, крейты, Cargo](modules-crates.md) — видимость, `pub use`,
    features, workspace, SemVer.
15. [Макросы](macros.md) — `macro_rules!`, процедурные макросы, гигиена,
    `cargo expand`.
16. [unsafe, UB и FFI](unsafe-ffi.md) — что именно разрешает `unsafe`,
    список UB, `extern "C"`, Miri.

### Конкурентность

17. [Потоки, Send и Sync](threads-send-sync.md) — потоки ОС, маркерные
    трейты, `scope`, каналы, `rayon`.
18. [Примитивы синхронизации и модель памяти](sync-primitives.md) — `Mutex`
    владеет данными, отравление, атомики и `Ordering`, дедлоки.
19. [async/await, Future и Tokio](async-await.md) — pull-модель, конечный
    автомат, рантайм вне языка, отмена и cancel safety, `Pin`.

### Практика

20. [Тестирование](testing.md) — юнит- и интеграционные тесты, doc-тесты,
    `criterion`, property-based, фаззинг.
21. [Инструменты, сборка, профилирование](tooling.md) — `rustup`, clippy,
    профили, LTO, flamegraph, `cargo audit`.
22. [Производительность и работа с памятью](performance.md) — аллокации,
    zero-cost abstractions, настройки release, `rayon`.
23. [Экосистема и типовой бэкенд-сервис](ecosystem-web.md) — serde, tokio,
    axum, sqlx, tracing, где Rust реально применяют.
24. [Идиомы и проектирование API](idioms-api-design.md) — newtype, typestate,
    builder, правила сигнатур, code smells.
25. [Типовые вопросы и задачи](interview-questions.md) — чек-лист для
    самопроверки и задачи на живое кодирование.

## Что Rust подсвечивает в остальных разделах

- [Rust ↔ остальные разделы: что стоит дописать](cross-language.md) — список
  доработок для `fundamentals/`, `python/`, `go/` и `sql/`, который виден
  именно с позиции Rust: владение и RAII, ошибки как значения, алгебраические
  типы, разница между гонкой данных и race condition.

## Базовые источники по всему разделу

- [The Rust Programming Language](https://doc.rust-lang.org/book/) — официальная книга, основной источник по языку.
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/) — те же темы через исполняемый код.
- [Rust Reference](https://doc.rust-lang.org/reference/) — формальное описание языка.
- [Rust Standard Library](https://doc.rust-lang.org/std/) — документация `std` с примерами на каждый метод.
- [Rustonomicon](https://doc.rust-lang.org/nomicon/) — небезопасный Rust, UB, раскладка данных.
- [Rust Atomics and Locks (Mara Bos)](https://marabos.nl/atomics/) — конкурентность и модель памяти.
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/) — проектирование публичного API.
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns/) — идиомы и антипаттерны.
- [The Rust Performance Book](https://nnethercote.github.io/perf-book/) — оптимизация кода и сборки.
- [This Week in Rust](https://this-week-in-rust.org/) — что меняется в языке и экосистеме.
