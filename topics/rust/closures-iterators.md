# Rust: замыкания и итераторы

[🏠 Карта тем по Rust](README.md)

## Что нужно знать

- **Замыкание — анонимная структура с захваченными полями** плюс реализация
  одного из трейтов: `FnOnce` (потребляет захваченное, вызывается один раз),
  `FnMut` (изменяет захваченное), `Fn` (только читает). Иерархия:
  каждое `Fn` — это `FnMut`, каждое `FnMut` — это `FnOnce`.
- **Захват выводится автоматически** — по ссылке, по изменяемой ссылке или по
  значению, в зависимости от использования. `move` заставляет захватить по
  значению; нужен для потоков и для замыканий, переживающих кадр стека.
  С издания 2021 захват идёт **по полям**, а не по всей структуре целиком.
- **У каждого замыкания уникальный анонимный тип**, поэтому их возвращают
  через `impl Fn(...)` либо `Box<dyn Fn(...)>`; указатели на функции
  (`fn(u32) -> u32`) — отдельный, более узкий тип, который приводится к `Fn`.
- **`Iterator` — трейт с одним обязательным методом `next`** и десятками
  дефолтных. Итераторы **ленивы**: цепочка `map`/`filter` ничего не делает,
  пока не вызван потребитель (`collect`, `sum`, `for`, `count`); отсюда
  предупреждение об «unused `Map`».
- **Три способа получить итератор**: `iter()` (`&T`), `iter_mut()` (`&mut T`),
  `into_iter()` (`T`). Для `for x in collection` вызывается `IntoIterator`.
- **Адаптеры, которые надо знать наизусть**: `map`, `filter`, `filter_map`,
  `flat_map`, `flatten`, `take`/`skip`, `take_while`/`skip_while`,
  `enumerate`, `zip`, `chain`, `rev` (нужен `DoubleEndedIterator`), `peekable`,
  `windows`/`chunks` (на срезах), `scan`, `fold`/`try_fold`, `any`/`all`,
  `find`/`position`, `min_by_key`/`max_by_key`, `sum`/`product`, `partition`,
  `collect`.
- **`collect` полиморфен по результату**: `Vec`, `String`, `HashMap`,
  `Result<Vec<_>, E>` (короткое замыкание на первой ошибке),
  `Option<Vec<_>>` — тип выбирается через `FromIterator`.
- **Zero-cost на практике**: цепочка адаптеров разворачивается в один цикл;
  типичный вопрос «что быстрее — цикл или итератор» имеет ответ «обычно
  одинаково, а итератор ещё и убирает проверку границ».
- **Свой итератор**: структура с состоянием + `impl Iterator`. Знать про
  `size_hint` (влияет на предвыделение в `collect`) и `ExactSizeIterator`.
- **Подвох**: `iter().map(...)` без потребителя ничего не выполняет;
  `for` по `Vec` по значению съедает вектор; замыкание с `move`, захватившее
  `Rc`, не станет `Send` — см. [потоки](threads-send-sync.md).

## Ссылки

- [Book: Closures](https://doc.rust-lang.org/book/ch13-01-closures.html) — три трейта и правила захвата.
- [Book: Iterators](https://doc.rust-lang.org/book/ch13-02-iterators.html) — ленивость и адаптеры.
- [std::iter::Iterator](https://doc.rust-lang.org/std/iter/trait.Iterator.html) — полный список методов.
- [Rust Reference: Closure types](https://doc.rust-lang.org/reference/types/closure.html) — как устроен захват, в том числе disjoint capture с издания 2021.
- [itertools](https://docs.rs/itertools) — адаптеры, которых нет в стандартной библиотеке.
