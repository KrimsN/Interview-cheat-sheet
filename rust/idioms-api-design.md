# Идиомы и проектирование API

[← Экосистема и типовой бэкенд-сервис](ecosystem-web.md) · [🏠 Домой](../README.md) · [Типовые вопросы и задачи →](interview-questions.md)

---

## Что значит «сделать некорректные состояния непредставимыми»?

**Коротко.** Главный проектный принцип в Rust: вместо проверок в рантайме
описать типы так, чтобы неправильное значение нельзя было построить. Enum
вместо флагов, newtype вместо голой строки, `Option` вместо «пустая строка
значит нет».

```rust
// плохо: представимы бессмысленные комбинации
struct BadConnection {
    connected: bool,
    session_id: Option<String>,
    error: Option<String>,   // connected = true и error = Some — что это значит?
}

// хорошо: каждое состояние несёт ровно свои данные
enum Connection {
    Disconnected,
    Connected { session_id: String },
    Failed { error: String },
}

// проверенные данные — отдельный тип
struct Email(String);

impl Email {
    fn parse(raw: &str) -> Result<Email, &'static str> {
        if raw.contains('@') { Ok(Email(raw.to_string())) } else { Err("нет @") }
    }
}

fn send(_to: &Email) { /* валидация уже не нужна: тип её гарантирует */ }

fn main() {
    match Email::parse("a@example.com") {
        Ok(e) => send(&e),
        Err(msg) => println!("{msg}"),
    }
    println!("{}", Email::parse("плохо").is_err());   // true
}
```

Ключевая мысль: если конструктор `Email::parse` — единственный способ
получить `Email`, то любая функция ниже по коду **уже не обязана** проверять
вход. Проверка происходит один раз на границе.

---

## Зачем нужен newtype?

**Коротко.** Он решает три задачи сразу: типобезопасность (перепутать
`UserId` и `OrderId` нельзя), обход [orphan rule](traits.md) и сокрытие
внутреннего представления. Цена в рантайме — нулевая.

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct UserId(u64);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct OrderId(u64);

fn cancel(order: OrderId) { println!("отменяю {order:?}"); }

fn main() {
    let u = UserId(7);
    let o = OrderId(7);
    // cancel(u);          // ошибка компиляции — а с голыми u64 это был бы баг в проде
    cancel(o);             // отменяю OrderId(7)
    println!("{}", u == UserId(7)); // true
}
```

**Подвох.** Newtype требует проброса нужных методов вручную. Соблазн
реализовать `Deref` и «унаследовать» всё — известный антипаттерн: получается
неявное API, где непонятно, чей метод вызывается. `Deref` предназначен для
умных указателей, а не для наследования.

---

## Что такое typestate?

**Коротко.** Состояние объекта кодируется в **типе**, а переходы — методы,
потребляющие `self` и возвращающие другой тип. Неправильный порядок вызовов
становится ошибкой компиляции.

```rust
struct Draft;
struct Sent;

struct Request<State> {
    url: String,
    _state: std::marker::PhantomData<State>,
}

impl Request<Draft> {
    fn new(url: &str) -> Self {
        Request { url: url.into(), _state: std::marker::PhantomData }
    }
    fn send(self) -> Request<Sent> {
        println!("отправляю {}", self.url);
        Request { url: self.url, _state: std::marker::PhantomData }
    }
}

impl Request<Sent> {
    fn read_response(&self) -> String { format!("ответ от {}", self.url) }
}

fn main() {
    let draft = Request::<Draft>::new("https://example.com");
    // draft.read_response();     // ошибка: метода нет у Request<Draft>
    let sent = draft.send();      // отправляю https://example.com
    println!("{}", sent.read_response()); // ответ от https://example.com
}
```

Это и есть ответ на вопрос «чем Rust отличается от языка с рантайм-проверками»:
там «нельзя читать ответ до отправки» — комментарий в документации и
исключение в рантайме, здесь — отсутствующий метод. `PhantomData` нужна,
чтобы параметр типа считался использованным; в рантайме она занимает 0 байт.

---

## Как заменяют именованные и опциональные аргументы?

**Коротко.** Их в языке нет — вместо них builder или структура настроек с
`Default`.

```rust
#[derive(Debug)]
struct Server { host: String, port: u16, workers: usize, tls: bool }

struct ServerBuilder { host: String, port: u16, workers: usize, tls: bool }

impl Server {
    fn builder() -> ServerBuilder {
        ServerBuilder { host: "127.0.0.1".into(), port: 8080, workers: 4, tls: false }
    }
}

impl ServerBuilder {
    fn port(mut self, p: u16) -> Self { self.port = p; self }
    fn tls(mut self, on: bool) -> Self { self.tls = on; self }
    fn build(self) -> Server {
        Server { host: self.host, port: self.port, workers: self.workers, tls: self.tls }
    }
}

fn main() {
    let s = Server::builder().port(443).tls(true).build();
    println!("{s:?}");
    // Server { host: "127.0.0.1", port: 443, workers: 4, tls: true }
}
```

Такой builder «по значению» (методы берут `self` и возвращают `Self`)
позволяет цепочку без временных переменных. Писать его руками не обязательно:
есть `derive_builder` и `bon`. Альтернатива попроще — публичная структура
настроек и синтаксис `..Default::default()` (см.
[стандартные трейты](std-traits.md)).

**Глубже.** `#[non_exhaustive]` на публичной структуре или enum запрещает
пользователям конструировать/сопоставлять их полностью — значит, добавление
поля или варианта не будет ломающим изменением. Для типов ошибок в
библиотеках это почти обязательная практика.

---

## Какие есть правила для сигнатур функций?

**Коротко.** Принимать максимально общее и заимствованное, возвращать
конкретное и владеющее.

| Вместо | Пишите | Почему |
|---|---|---|
| `&String` | `&str` | больше вызывающих, нет лишней косвенности |
| `&Vec<T>` | `&[T]` | примет и массив, и часть буфера |
| `&PathBuf` | `impl AsRef<Path>` | примет `&str`, `String`, `Path` |
| `Box<dyn Trait>` в возврате | `impl Trait` | без аллокации и косвенного вызова |
| `fn get(&self) -> Option<&T>` | так и оставить | не паниковать за пользователя |

```rust
use std::path::Path;

// принимает почти всё, возвращает владеющее значение
fn read_lines(path: impl AsRef<Path>) -> std::io::Result<Vec<String>> {
    Ok(std::fs::read_to_string(path)?.lines().map(str::to_owned).collect())
}

fn main() {
    println!("{}", read_lines("Cargo.toml").map(|v| v.len()).unwrap_or(0) > 0);
}
```

---

## Как в Rust принято именовать методы?

**Коротко.** Соглашение из API Guidelines, и его знание проверяют:

| Префикс | Смысл | Пример |
|---|---|---|
| `new`, `with_*` | конструкторы | `Vec::new`, `Vec::with_capacity` |
| `as_*` | дешёвое заимствование | `String::as_str` |
| `to_*` | дорогое копирование | `str::to_owned` |
| `into_*` | потребляет `self` | `String::into_bytes` |
| `is_*`, `has_*` | предикаты, возвращают `bool` | `Option::is_some` |
| `try_*` | версия, возвращающая `Result` | `TryFrom::try_from` |
| `iter`, `iter_mut`, `into_iter` | три вида итерации | см. [итераторы](closures-iterators.md) |

Соблюдение этих правил делает API предсказуемым: увидев `into_inner`,
пользователь без документации понимает, что объект будет потреблён.

Из тех же соображений: `Default` вместо конструктора без аргументов,
`From` вместо `new_from_json`, `Display` вместо метода `to_pretty_string`.

---

## Что в Rust-коде считается code smell?

**Коротко.** Признаки того, что боролись с компилятором вместо проектирования:

- **россыпь `clone()`** — обычно значит, что структура владения не продумана;
  один осознанный `clone` нормален, десять в одной функции — сигнал;
- **`unwrap()` в библиотечном коде** — паника вместо `Result` у пользователя;
- **`Rc<RefCell<T>>` там, где хватило бы владения** — попытка воспроизвести
  привычки языка с GC; часто лечится ареной с индексами (см. [умные
  указатели](smart-pointers.md));
- **«ООП-код»**: трейт с единственной реализацией ради «интерфейса»,
  попытка наследования через супертрейты и `Deref`;
- **преждевременный `unsafe`** ради воображаемой скорости, без бенчмарка;
- **глобальное изменяемое состояние** через `static mut` вместо `OnceLock`
  или передачи состояния явно;
- **лайфтаймы там, где хватило бы владения**: `struct Config<'a>` с полями
  `&'a str` заражает временем жизни всё приложение.

**Подвох.** Обратная крайность тоже смелл: увлечение обобщениями и
типовым программированием там, где хватило бы обычной структуры. Хороший
Rust-код скучный.

---

## Что относится к API-гигиене библиотеки?

**Коротко.** Документация с проверяемыми примерами, `#[must_use]`,
осторожность с публичной поверхностью, `#[non_exhaustive]` на ошибках.

```rust
#![deny(missing_docs)]                     // публичный элемент без /// — ошибка сборки

/// Идентификатор пользователя.
///
/// ```
/// # use my_crate::UserId;
/// assert_eq!(UserId::new(7).get(), 7);
/// ```
#[must_use = "идентификатор бесполезно создавать и не использовать"]
pub struct UserId(u64);
```

Практические правила:

- всё приватно, пока не доказано обратное: убрать `pub` потом — ломающее
  изменение;
- `pub use` как фасад, чтобы внутренняя раскладка модулей не стала частью
  API ([модули](modules-crates.md));
- примеры в `///` проверяются `cargo test` — документация не протухает
  ([тестирование](testing.md));
- SemVer соблюдают строго: добавление публичного поля в структуру, нового
  варианта в enum или новой границы в дженерик — ломающие изменения.

---

[← Экосистема и типовой бэкенд-сервис](ecosystem-web.md) · [🏠 Домой](../README.md) · [Типовые вопросы и задачи →](interview-questions.md)
