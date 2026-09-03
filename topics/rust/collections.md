# Rust: коллекции стандартной библиотеки

[🏠 Карта тем по Rust](README.md)

## Что нужно знать

- **`Vec<T>`** — динамический массив: указатель, длина, ёмкость. Рост
  амортизированный (обычно удвоение), при реаллокации элементы перемещаются, а
  все ссылки на них инвалидируются — это и есть причина, по которой borrow
  checker запрещает держать `&T` во время `push`.
- **`with_capacity`, `reserve`, `shrink_to_fit`** — управление ёмкостью;
  `Vec::new` не выделяет память вовсе. `into_boxed_slice` отдаёт лишнюю
  ёмкость.
- **Срезы `&[T]` / `&mut [T]`** — общий интерфейс к `Vec`, массиву и части
  буфера. Функции лучше принимать срез, а не `&Vec<T>`.
- **`HashMap<K, V>`**: хеширование SipHash 1-3 со случайным ключом на процесс
  (защита от HashDoS), поэтому порядок итерации не определён и меняется между
  запусками; для скорости — `ahash`/`rustc-hash`, для детерминизма —
  `BTreeMap`.
- **Entry API** — идиоматическая замена «проверил, потом вставил»:
  `map.entry(k).or_insert_with(Vec::new).push(v)`; одна операция вместо двух
  и без двойного заимствования.
- **`BTreeMap`/`BTreeSet`** — упорядоченные (B-дерево, требует `Ord`),
  поддерживают диапазонные запросы `range(a..b)`; `HashMap`/`HashSet` —
  амортизированный O(1) без порядка.
- **Ключи**: `Hash` + `Eq` должны быть согласованы (равные значения — равный
  хеш) и **не должны меняться, пока ключ в коллекции** — иначе элемент
  «теряется». Логическая, а не memory-safety проблема; ровно как в Python и
  Java.
- **`VecDeque`** — кольцевой буфер, O(1) с обоих концов; `BinaryHeap` —
  двоичная куча (max-heap, для min-heap оборачивают в `Reverse`);
  `LinkedList` — есть, но почти всегда не нужен.
- **Итерация в трёх видах**: `iter()` даёт `&T`, `iter_mut()` — `&mut T`,
  `into_iter()` — `T` с потреблением коллекции. Для `&Vec<T>` в цикле `for`
  автоматически выбирается `iter()`.
- **Полезные методы вместо ручных циклов**: `retain`, `drain`, `dedup`,
  `sort_by_key`/`sort_unstable`, `binary_search`, `chunks`, `windows`,
  `split_at_mut`, `swap_remove` (O(1) удаление без сохранения порядка).
- **`HashMap::get` возвращает `Option<&V>`** — индексация `map[&k]` паникует;
  это отличие от Python, где `dict[k]` бросает `KeyError`, и от Go, где
  отсутствующий ключ даёт нулевое значение.

## Ссылки

- [std::collections](https://doc.rust-lang.org/std/collections/index.html) — обзор всех коллекций и таблица «какую выбрать».
- [Book: Common Collections](https://doc.rust-lang.org/book/ch08-00-common-collections.html) — `Vec`, `String`, `HashMap` с примерами.
- [std::collections::hash_map::Entry](https://doc.rust-lang.org/std/collections/hash_map/enum.Entry.html) — entry API целиком.
- [std::vec::Vec](https://doc.rust-lang.org/std/vec/struct.Vec.html) — гарантии по ёмкости и реаллокации.
- [The Rust Performance Book: Collections](https://nnethercote.github.io/perf-book/hashing.html) — выбор хешера и цена аллокаций.
