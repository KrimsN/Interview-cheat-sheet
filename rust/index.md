# Rust — шпаргалка для собеседований

[🏠 Домой](../README.md) · [Базовый синтаксис и модель языка →](basics.md)

---

Темы в порядке чтения — от модели владения к конкурентности, async и
практике. Каждая тема построена как «вопрос → ответ»: **Коротко** — модель
устного ответа, дальше разбор, рабочий пример, **Подвох** и **Глубже**.
Языконезависимая теория (ООП, SOLID, паттерны, архитектура, конкурентность
как концепция) — в [fundamentals/](../fundamentals/index.md).

### Язык

1. [Базовый синтаксис и модель языка](basics.md) — `let` и иммутабельность, выражения, shadowing, editions
2. [Владение, перемещение и Drop](ownership.md) — три правила, move-семантика, `Copy` против `Clone`, RAII
3. [Заимствование, ссылки и времена жизни](borrowing-lifetimes.md) — «shared XOR mutable», NLL, elision, `'static`
4. [Типы, представление в памяти, Sized](types-memory-layout.md) — переполнение, `repr`, niche-оптимизация, DST
5. [Строки, срезы и Cow](strings.md) — `String` против `&str`, UTF-8, `OsString`/`CString`, clone-on-write
6. [Коллекции стандартной библиотеки](collections.md) — `Vec`, `HashMap`, entry API, `BTreeMap`, реаллокация
7. [Перечисления и сопоставление с образцом](enums-pattern-matching.md) — типы-суммы, `Option`, исчерпывающий `match`
8. [Обработка ошибок](error-handling.md) — `Result`, оператор `?`, `thiserror`/`anyhow`, когда уместна паника
9. [Трейты](traits.md) — явная реализация, orphan rule, ассоциированные типы, `dyn` и object safety
10. [Дженерики и мономорфизация](generics-monomorphization.md) — границы, `impl Trait`, const generics, цена абстракции
11. [Замыкания и итераторы](closures-iterators.md) — `Fn`/`FnMut`/`FnOnce`, ленивость, адаптеры, `collect`
12. [Умные указатели и внутренняя изменяемость](smart-pointers.md) — `Box`, `Rc`/`Arc`, `RefCell`, `Weak`, `Deref`
13. [Стандартные трейты и преобразования](std-traits.md) — `From`/`Into`, `Display`/`Debug`, `Ord`/`Hash`, `Default`
14. [Модули, крейты, Cargo](modules-crates.md) — видимость, `pub use`, features, workspace, SemVer
15. [Макросы](macros.md) — `macro_rules!`, процедурные макросы, гигиена, `cargo expand`
16. [unsafe, UB и FFI](unsafe-ffi.md) — что разрешает `unsafe`, список UB, `extern "C"`, Miri

### Конкурентность

17. [Потоки, Send и Sync](threads-send-sync.md) — потоки ОС, маркерные трейты, `scope`, каналы, `rayon`
18. [Примитивы синхронизации и модель памяти](sync-primitives.md) — `Mutex` владеет данными, отравление, атомики, дедлоки
19. [async/await, Future и Tokio](async-await.md) — pull-модель, конечный автомат, отмена и cancel safety, `Pin`

### Практика

20. [Тестирование](testing.md) — юнит- и интеграционные тесты, doc-тесты, `criterion`, property-based
21. [Инструменты, сборка, профилирование](tooling.md) — `rustup`, clippy, профили, LTO, flamegraph, `cargo audit`
22. [Производительность и работа с памятью](performance.md) — аллокации, zero-cost abstractions, настройки release
23. [Экосистема и типовой бэкенд-сервис](ecosystem-web.md) — serde, tokio, axum, sqlx, tracing
24. [Идиомы и проектирование API](idioms-api-design.md) — newtype, typestate, builder, правила сигнатур, code smells
25. [Типовые вопросы и задачи](interview-questions.md) — чек-лист для самопроверки и задачи на живое кодирование

Черновая карта тем со ссылками на официальную документацию по каждому пункту —
в [topics/rust/](../topics/rust/README.md).

---

[🏠 Домой](../README.md) · [Базовый синтаксис и модель языка →](basics.md)
