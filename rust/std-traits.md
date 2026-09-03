# Стандартные трейты и преобразования

[← Умные указатели](smart-pointers.md) · [🏠 Домой](../README.md) · [Модули, крейты, Cargo →](modules-crates.md)

---

## Как устроены преобразования типов: `From`, `Into`, `TryFrom`, `FromStr`?

**Коротко.** Реализуют всегда `From`, а `Into` приходит автоматически из
blanket impl. Для преобразований, которые могут не удаться, — `TryFrom`
(возвращает `Result`). Для разбора из строки — `FromStr`, за которым стоит
метод `parse`.

```rust
struct Celsius(f64);
struct Fahrenheit(f64);

impl From<Celsius> for Fahrenheit {
    fn from(c: Celsius) -> Self { Fahrenheit(c.0 * 9.0 / 5.0 + 32.0) }
}

fn main() {
    let f: Fahrenheit = Celsius(100.0).into();   // Into бесплатно из From
    println!("{:.1}", f.0);                       // 212.0

    let ok = u8::try_from(200i32);
    let bad = u8::try_from(300i32);
    println!("{ok:?} {}", bad.is_err());          // Ok(200) true

    let n: i32 = "42".parse().unwrap();           // FromStr
    println!("{n}");                              // 42
}
```

Правило для сигнатур: принимать `impl Into<T>` удобно вызывающему (он передаст
и `&str`, и `String`), возвращать — конкретный тип.

**Подвох.** Реализовать `Into` напрямую нельзя (точнее, можно, но не нужно):
из-за blanket impl `impl<T, U: From<T>> Into<U> for T` он появится сам, а
ручная реализация вступит в конфликт. Это классический вопрос «почему я
реализую `From`, а не `Into`».

---

## Чем `Display` отличается от `Debug`?

**Коротко.** `Debug` (`{:?}`) — для разработчика, выводится через
`#[derive(Debug)]`, печатает структуру как есть. `Display` (`{}`) — для
пользователя, пишется только руками, потому что универсального правила
«человеческого» представления не существует.

```rust
use std::fmt;

#[derive(Debug)]
struct Money { amount: i64, currency: &'static str }

impl fmt::Display for Money {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}.{:02} {}", self.amount / 100, self.amount % 100, self.currency)
    }
}

fn main() {
    let m = Money { amount: 12345, currency: "RUB" };
    println!("{m}");        // 123.45 RUB
    println!("{m:?}");      // Money { amount: 12345, currency: "RUB" }
    println!("{m:#?}");     // многострочный «pretty» вывод
    println!("{}", m.to_string()); // 123.45 RUB — ToString пришёл из blanket impl
}
```

**Подвох.** `ToString` вручную не реализуют: он появляется автоматически у
всего, что реализует `Display`. Реализовать оба — конфликт когерентности.

**Глубже.** У `Formatter` есть флаги ширины, точности и выравнивания
(`{:>10}`, `{:.2}`); их поддерживают через `f.pad(...)`, если хотите, чтобы
`{:>10}` работало и для вашего типа. `#[derive(Debug)]` это делает сам.

---

## Что нужно знать про `PartialEq`/`Eq` и `PartialOrd`/`Ord`?

**Коротко.** Пара «частичный/полный» разделена из-за чисел с плавающей точкой:
`NaN != NaN`, поэтому `f64` реализует только `PartialEq` и `PartialOrd`, но
не `Eq` и не `Ord`.

```rust
#[derive(PartialEq, Eq, PartialOrd, Ord, Debug)]
struct Version { major: u32, minor: u32 }  // сравнение лексикографическое по полям

fn main() {
    let mut vs = vec![
        Version { major: 1, minor: 9 },
        Version { major: 1, minor: 2 },
    ];
    vs.sort();
    println!("{vs:?}");   // [Version { major: 1, minor: 2 }, Version { major: 1, minor: 9 }]

    let mut floats = vec![3.5, f64::NAN, 1.0];
    // floats.sort();                      // ошибка: f64 не реализует Ord
    floats.sort_by(|a, b| a.total_cmp(b)); // total_cmp — полный порядок, NaN в конце
    println!("{:?}", &floats[..2]);        // [1.0, 3.5]
}
```

Правило согласованности: `Hash` обязан соответствовать `Eq` — равные значения
дают равный хеш. Иначе элементы «теряются» в
[`HashMap`](collections.md). Поэтому `derive` их обычно ставят вместе.

**Глубже.** `#[derive(PartialOrd, Ord)]` сравнивает поля **в порядке
объявления**, лексикографически. Это удобно и опасно одновременно:
перестановка полей молча меняет семантику сортировки. Если порядок важен —
пишут `impl Ord` вручную и оставляют комментарий.

---

## Зачем `Default` и как его используют?

**Коротко.** `Default::default()` — «пустое/нулевое» значение типа. Основной
приём — структура настроек плюс синтаксис обновления
`..Default::default()`.

```rust
#[derive(Debug, Default)]
struct ServerConfig {
    host: String,      // ""
    port: u16,         // 0
    tls: bool,         // false
    workers: usize,    // 0
}

#[derive(Debug, Default, PartialEq)]
enum Mode { #[default] Fast, Careful }

fn main() {
    let cfg = ServerConfig {
        port: 8080,
        ..Default::default()      // остальные поля — по умолчанию
    };
    println!("{cfg:?}");          // ServerConfig { host: "", port: 8080, tls: false, workers: 0 }
    println!("{:?}", Mode::default()); // Fast
}
```

`Default` требуется многим функциям стандартной библиотеки:
`unwrap_or_default`, `HashMap::entry(...).or_default()`, `mem::take`.

**Подвох.** Умолчание «ноль» бывает бессмысленным: `workers: 0` или
`timeout: 0` — не разумные значения, а мина. Если умолчание нетривиально,
`Default` реализуют вручную, а не выводят derive.

---

## В чём разница между `AsRef`, `Borrow` и `Deref`?

**Коротко.** `AsRef<T>` — дешёвое явное преобразование ссылки, без
дополнительных обещаний. `Borrow<T>` — то же самое, но с гарантией, что
`Hash`/`Eq`/`Ord` заимствованной формы совпадают с оригиналом. `Deref` —
неявное приведение, которое вставляет компилятор.

```rust
use std::collections::HashMap;
use std::path::Path;

fn read(path: impl AsRef<Path>) -> String {
    format!("читаю {}", path.as_ref().display())   // принимает &str, String, PathBuf
}

fn main() {
    println!("{}", read("a.txt"));                  // читаю a.txt

    let mut m: HashMap<String, i32> = HashMap::new();
    m.insert("ключ".into(), 1);
    println!("{:?}", m.get("ключ"));   // Some(1) — ищем по &str в карте с ключами String
}
```

Последняя строка работает именно из-за `Borrow`: сигнатура
`get<Q>(&self, k: &Q) where String: Borrow<Q>` требует, чтобы хеш `&str`
совпадал с хешем `String`. С `AsRef` такой гарантии нет, и метод был бы
некорректен.

**Глубже.** `ToOwned` — обобщение `Clone` на заимствованные типы: `&str →
String`, `&[T] → Vec<T>`. Именно он стоит за `Cow` (см.
[строки](strings.md)) и за методом `to_owned()`, который стоит предпочитать
`to_string()` там, где смысл — «сделать владеющую копию», а не
«отформатировать».

---

## Как перегружают операторы?

**Коротко.** Через трейты из `std::ops`: `Add`, `Sub`, `Mul`, `Neg`, `Not`,
`Index`/`IndexMut`, `AddAssign`. Произвольных операторов, как в C++, придумать
нельзя — только реализовать существующие.

```rust
use std::ops::{Add, Index};

#[derive(Debug, Clone, Copy)]
struct Vec2 { x: f64, y: f64 }

impl Add for Vec2 {
    type Output = Vec2;
    fn add(self, rhs: Vec2) -> Vec2 { Vec2 { x: self.x + rhs.x, y: self.y + rhs.y } }
}

impl Index<usize> for Vec2 {
    type Output = f64;
    fn index(&self, i: usize) -> &f64 {
        match i { 0 => &self.x, 1 => &self.y, _ => panic!("индекс вне диапазона") }
    }
}

fn main() {
    let a = Vec2 { x: 1.0, y: 2.0 };
    let b = Vec2 { x: 3.0, y: 4.0 };
    let c = a + b;
    println!("{:?} {}", c, c[0]);   // Vec2 { x: 4.0, y: 6.0 } 4
}
```

**Подвох.** `Add` по умолчанию **потребляет** операнды (`self`, не `&self`).
Для типов, которые не `Copy`, обычно дополнительно реализуют
`impl Add<&Vec2> for &Vec2`, иначе `a + b` съест оба вектора.

---

## Какие derive-макросы ставят почти всегда?

**Коротко.** `#[derive(Debug, Clone, PartialEq)]` — базовый набор; для ключей
карт добавляют `Eq, Hash`; для настроек — `Default`; для сериализации —
`serde::{Serialize, Deserialize}`.

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash, Default)]
struct UserId(u64);
```

Соображения при выборе:

- `Debug` — почти всегда, иначе тип нельзя напечатать в логе и в тесте;
- `Clone` — если тип должны копировать пользователи; `Copy` — только для
  маленьких значений без владения ([владение](ownership.md));
- `PartialEq` — нужен для `assert_eq!` в тестах;
- `Hash + Eq` — если тип может стать ключом карты;
- `Serialize/Deserialize` — на границе сервиса.

**Глубже.** `derive` для обобщённых типов добавляет границу на **каждый**
параметр: `#[derive(Clone)] struct W<T>(T)` порождает `impl<T: Clone> Clone
for W<T>`. Иногда это лишнее (например, `W<T>` мог бы быть `Clone` и без
`T: Clone`, если внутри `Arc<T>`) — тогда реализацию пишут вручную. Это
известное ограничение derive-макросов, и вопрос про него любят задавать.

---

[← Умные указатели](smart-pointers.md) · [🏠 Домой](../README.md) · [Модули, крейты, Cargo →](modules-crates.md)
