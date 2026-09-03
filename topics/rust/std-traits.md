# Rust: стандартные трейты и преобразования

[🏠 Карта тем по Rust](README.md)

## Что нужно знать

- **Преобразования**: `From`/`Into` (инфаллибельные, реализуют `From`, а
  `Into` приходит автоматически через blanket impl), `TryFrom`/`TryInto`
  (возвращают `Result`), `FromStr` (`"42".parse::<i32>()`), `ToString`
  (появляется сам у всего, что реализует `Display`).
- **Печать**: `Display` — для пользователя, пишется вручную; `Debug` —
  для разработчика, обычно `#[derive(Debug)]`, форматируется `{:?}` и `{:#?}`.
  `Display` нельзя вывести derive-макросом намеренно: у «человеческого»
  представления нет универсального правила.
- **Сравнение**: `PartialEq`/`Eq`, `PartialOrd`/`Ord`. `f64` — только
  `PartialEq`/`PartialOrd`, потому что `NaN` нарушает рефлексивность; отсюда
  `sort_by(|a, b| a.partial_cmp(b).unwrap())` и `total_cmp`. `Hash` должен
  быть согласован с `Eq`.
- **`Default`** — нулевое/пустое значение, `#[derive(Default)]`, для enum —
  `#[default]` на варианте; часто используется в паттерне «структура
  настроек + `..Default::default()`».
- **Заимствование и разыменование**: `Deref`, `AsRef`/`AsMut`, `Borrow`/
  `BorrowMut`. Разница `AsRef` и `Borrow` — тонкий вопрос: `Borrow` требует,
  чтобы заимствованная форма имела те же `Eq`/`Hash` (поэтому
  `HashMap<String, _>::get` принимает `&str`).
- **Итерирование**: `Iterator`, `IntoIterator` (три реализации: для `T`,
  `&T`, `&mut T`), `FromIterator` (за `collect`), `Extend`.
- **Операторы**: `Add`, `Sub`, `Mul`, `Neg`, `Index`/`IndexMut`, `Not` —
  перегрузка операторов через трейты из `std::ops`; `Fn`-трейты — тоже
  операторная перегрузка вызова.
- **Маркеры**: `Copy`, `Send`, `Sync`, `Sized`, `Unpin` — реализуются
  автоматически (auto traits) и снимаются наличием «неподходящего» поля.
- **Жизненный цикл**: `Clone`, `Drop`, `ToOwned` (`&str -> String`,
  обобщение `Clone` для DST).
- **Правило API**: принимать максимально общий тип (`impl AsRef<Path>`,
  `impl IntoIterator<Item = T>`), возвращать конкретный.
- **Derive-макросы, которые пишут почти всегда**:
  `#[derive(Debug, Clone, PartialEq)]`; для ключей карт добавляют `Eq, Hash`;
  для сериализации — `serde::{Serialize, Deserialize}`.

## Ссылки

- [std::convert](https://doc.rust-lang.org/std/convert/index.html) — `From`, `Into`, `TryFrom`, `AsRef`.
- [std::fmt](https://doc.rust-lang.org/std/fmt/index.html) — синтаксис форматирования и трейты печати.
- [std::cmp](https://doc.rust-lang.org/std/cmp/index.html) — семантика `Eq`/`Ord` и частичных сравнений.
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/) — какие трейты обязан реализовать публичный тип.
- [std::borrow::Borrow](https://doc.rust-lang.org/std/borrow/trait.Borrow.html) — разбор отличия от `AsRef`.
