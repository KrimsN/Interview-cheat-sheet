# Замыкания и итераторы

[← Дженерики и мономорфизация](generics-monomorphization.md) · [🏠 Домой](../README.md) · [Умные указатели и внутренняя изменяемость →](smart-pointers.md)

---

## Что такое замыкание с точки зрения компилятора?

**Коротко.** Анонимная структура с полями — захваченными переменными — плюс
реализация одного из трейтов `FnOnce`, `FnMut` или `Fn`. Никакой магии: вызов
замыкания — это вызов метода этой структуры.

```rust
fn main() {
    let factor = 3;
    let scale = |x: i32| x * factor;   // ≈ struct Anon { factor: i32 } + impl Fn
    println!("{}", scale(14));         // 42
}
```

Иерархия трейтов вложенная: каждое `Fn` является `FnMut`, каждое `FnMut` —
`FnOnce`.

| Трейт | Как получает `self` | Что делает с захваченным |
|---|---|---|
| `FnOnce` | `self` | потребляет — вызвать можно один раз |
| `FnMut` | `&mut self` | изменяет |
| `Fn` | `&self` | только читает |

```rust
fn call_twice(f: impl Fn() -> i32) -> i32 { f() + f() }
fn call_mut(mut f: impl FnMut()) { f(); f(); }
fn call_once(f: impl FnOnce() -> String) -> String { f() }

fn main() {
    let base = 10;
    println!("{}", call_twice(|| base));      // 20 — только читает

    let mut count = 0;
    call_mut(|| count += 1);                  // изменяет захваченное
    println!("{count}");                      // 2

    let owned = String::from("съедено");
    println!("{}", call_once(move || owned)); // съедено — значение уехало наружу
}
```

**Подвох.** Какой трейт реализует замыкание, определяет не автор, а
**компилятор** — по тому, что делает тело. Поэтому «сделай его `Fn`» означает
«перестань изменять и потреблять захваченное».

---

## Как замыкание захватывает переменные и зачем `move`?

**Коротко.** Компилятор выбирает минимально необходимый способ захвата: по
`&`, по `&mut` или по значению. `move` принудительно требует захвата по
значению — это нужно, когда замыкание переживает кадр стека: поток,
async-задача, возвращаемое значение.

```rust
use std::thread;

fn main() {
    let data = vec![1, 2, 3];

    // без move поток мог бы пережить data — компилятор не разрешит
    let h = thread::spawn(move || data.iter().sum::<i32>());
    println!("{}", h.join().unwrap());   // 6

    let mut log = Vec::new();
    let mut record = |s: &str| log.push(s.to_string()); // захват по &mut
    record("a");
    record("b");
    // println!("{log:?}");              // ошибка: log ещё заимствован
    drop(record);
    println!("{log:?}");                 // ["a", "b"]
}
```

**Глубже.** С издания 2021 захват идёт **по отдельным полям**, а не по всей
структуре: замыкание, использующее только `cfg.name`, захватит именно поле, а
не весь `cfg`. Это заметно снимает часть былых схваток с borrow checker.

**Подвох.** `move` не означает «копировать всё»: для `Copy`-типов он
захватывает копию, для остальных перемещает владение. И `move`-замыкание,
захватившее `Rc`, не станет `Send` — в поток его не отправить (см.
[потоки](threads-send-sync.md)).

---

## Как вернуть замыкание из функции?

**Коротко.** У каждого замыкания уникальный анонимный тип, назвать который
нельзя. Поэтому: `impl Fn(...)` — если тип один; `Box<dyn Fn(...)>` — если
из разных веток возвращаются разные замыкания.

```rust
fn adder(n: i32) -> impl Fn(i32) -> i32 { move |x| x + n }

fn op(name: &str) -> Box<dyn Fn(i32) -> i32> {
    match name {
        "inc" => Box::new(|x| x + 1),
        "dbl" => Box::new(|x| x * 2),
        _ => Box::new(|x| x),
    }
}

fn apply(f: fn(i32) -> i32, x: i32) -> i32 { f(x) }   // указатель на функцию

fn double(x: i32) -> i32 { x * 2 }

fn main() {
    println!("{}", adder(2)(40));      // 42
    println!("{}", op("dbl")(21));     // 42
    println!("{}", apply(double, 21)); // 42
    println!("{}", apply(|x| x * 2, 21)); // 42 — замыкание без захвата приводится к fn
}
```

**Глубже.** `fn(i32) -> i32` (указатель на функцию) — отдельный, более узкий
тип: он не хранит захваченного состояния, зато является `Copy`, `Send`,
`Sync` и передаётся в C-код. Замыкание без захватов автоматически приводится к
нему, с захватами — нет.

---

## Что такое `Iterator` и почему итераторы ленивы?

**Коротко.** `Iterator` — трейт с единственным обязательным методом
`next(&mut self) -> Option<Self::Item>` и десятками дефолтных методов поверх
него. Адаптеры (`map`, `filter`) не вычисляют ничего — они возвращают новый
итератор; работа начинается, когда его потребят (`collect`, `sum`, `for`,
`count`).

```rust
fn main() {
    let v = vec![1, 2, 3, 4, 5];

    let lazy = v.iter().map(|x| { println!("считаем {x}"); x * 2 });
    println!("пока ничего не напечаталось");
    let result: Vec<i32> = lazy.collect(); // вот теперь выполняется
    println!("{result:?}");
    // пока ничего не напечаталось
    // считаем 1 ... считаем 5
    // [2, 4, 6, 8, 10]
}
```

Ленивость даёт две вещи: бесконечные последовательности
(`(1..).filter(...).take(5)`) и слияние проходов — цепочка из пяти адаптеров
всё равно обходит данные один раз.

**Подвох.** Забытый потребитель — типичная ошибка: `v.iter().map(|x| do_it(x));`
не выполнится вообще, компилятор предупредит «unused `Map` that must be
used». Если нужен именно побочный эффект, пишут `for` или `for_each`.

---

## Какие адаптеры нужно знать наизусть?

**Коротко.** `map`, `filter`, `filter_map`, `flat_map`, `take`/`skip`,
`enumerate`, `zip`, `chain`, `rev`, `fold`, `any`/`all`, `find`/`position`,
`min_by_key`/`max_by_key`, `sum`, `partition`, `collect`.

```rust
fn main() {
    let words = ["10", "x", "20", "30"];

    // filter_map = filter + map за один проход
    let nums: Vec<i32> = words.iter().filter_map(|s| s.parse().ok()).collect();
    println!("{nums:?}");                        // [10, 20, 30]

    let total: i32 = nums.iter().sum();
    println!("{total}");                          // 60

    println!("{:?}", nums.iter().max_by_key(|&&x| x));      // Some(30)
    println!("{:?}", nums.iter().position(|&x| x == 20));   // Some(1)
    println!("{}", nums.iter().any(|&x| x > 25));           // true

    let (big, small): (Vec<i32>, Vec<i32>) = nums.iter().partition(|&&x| x >= 20);
    println!("{big:?} {small:?}");                // [20, 30] [10]

    // fold — обобщение всех сверток
    let joined = nums.iter().fold(String::new(), |mut acc, x| {
        if !acc.is_empty() { acc.push(','); }
        acc.push_str(&x.to_string());
        acc
    });
    println!("{joined}");                         // 10,20,30

    // zip + enumerate
    for (i, (a, b)) in nums.iter().zip(words.iter()).enumerate().take(2) {
        print!("{i}:{a}/{b} ");                   // 0:10/10 1:20/x
    }
    println!();
}
```

**Глубже.** `rev()` требует `DoubleEndedIterator` (итератор умеет ходить с
конца) — поэтому он работает для `Vec` и диапазонов, но не для итератора по
`HashMap`. `peekable()` даёт `peek()` для парсеров, `scan` — `fold` с
промежуточными результатами.

---

## Во что умеет собирать `collect`?

**Коротко.** Во всё, для чего реализован `FromIterator`: `Vec`, `String`,
`HashMap`, `HashSet`, `BTreeMap`, а также — что важнее всего —
`Result<Vec<_>, E>` и `Option<Vec<_>>`.

```rust
use std::collections::HashMap;

fn main() {
    let pairs = [("a", 1), ("b", 2)];
    let map: HashMap<&str, i32> = pairs.into_iter().collect();
    println!("{}", map["b"]);                            // 2

    let s: String = ["раз", "два"].into_iter().collect();
    println!("{s}");                                     // раздва

    // Result «выворачивается наизнанку»: Vec<Result<T,E>> -> Result<Vec<T>,E>
    let ok: Result<Vec<i32>, _> = ["1", "2"].iter().map(|s| s.parse::<i32>()).collect();
    let bad: Result<Vec<i32>, _> = ["1", "x"].iter().map(|s| s.parse::<i32>()).collect();
    println!("{ok:?} {}", bad.is_err());                 // Ok([1, 2]) true
}
```

Сборка в `Result` делает короткое замыкание: на первой ошибке обход
прекращается. Это идиоматичная замена циклу с ручной проверкой — см.
[обработку ошибок](error-handling.md).

---

## Как написать собственный итератор?

**Коротко.** Структура с состоянием плюс `impl Iterator` с методом `next`.
Все адаптеры появятся автоматически из дефолтных методов трейта.

```rust
struct Fib { a: u64, b: u64 }

impl Iterator for Fib {
    type Item = u64;

    fn next(&mut self) -> Option<u64> {
        let out = self.a;
        self.a = self.b;
        self.b = out + self.b;
        Some(out)          // бесконечный итератор — None не возвращаем никогда
    }
}

fn main() {
    let f = Fib { a: 0, b: 1 };
    println!("{:?}", f.take(8).collect::<Vec<_>>()); // [0, 1, 1, 2, 3, 5, 8, 13]
}
```

**Глубже.** Стоит переопределить `size_hint`, если размер известен: `collect`
использует его для предвыделения буфера, и это заметно экономит аллокации.
Если размер известен точно — реализуют ещё и `ExactSizeIterator` (даёт
`len()`), а для обхода с конца — `DoubleEndedIterator` (даёт `rev()`).

**Подвох.** Чтобы `for x in MyCollection` работал, реализуют не `Iterator` для
коллекции, а `IntoIterator` — обычно три реализации: для `T` (потребляющая),
`&T` (по ссылкам) и `&mut T`. Именно так `Vec` даёт три разных поведения в
цикле `for`.

---

[← Дженерики и мономорфизация](generics-monomorphization.md) · [🏠 Домой](../README.md) · [Умные указатели и внутренняя изменяемость →](smart-pointers.md)
