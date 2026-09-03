# Rust: строки, срезы и Cow

[🏠 Карта тем по Rust](README.md)

## Что нужно знать

- **Два основных типа**: `String` — владеющий растущий буфер UTF-8 в куче;
  `&str` — заимствованный срез валидного UTF-8 (адрес + длина в **байтах**).
  Литерал `"abc"` имеет тип `&'static str`.
- **Правило API**: принимайте `&str`, возвращайте `String` (или `Cow`).
  Для обобщения — `impl AsRef<str>` или `impl Into<String>` в зависимости от
  того, нужно ли владение.
- **Индексации по символам нет**: `s[0]` не компилируется, потому что байт —
  не символ. Есть срезы по байтовым границам (паника, если граница разрезает
  кодовую точку), итерация `chars()`, `char_indices()`, `bytes()`. Графемных
  кластеров в стандартной библиотеке нет — это крейт
  `unicode-segmentation`.
- **`len()` — в байтах**, `chars().count()` — в кодовых точках за O(n), и ни
  то, ни другое не равно числу символов, как их видит человек (эмодзи с
  модификаторами, `é` в разложенной форме).
- **Сборка строк**: `push_str`/`push`, `format!`, `String::with_capacity`,
  `concat`/`join` для срезов. Оператор `+` перемещает левый операнд.
- **Другие строковые типы и когда они нужны**: `OsString`/`OsStr` — строки ОС
  (пути в Windows не всегда валидный UTF-8), `Path`/`PathBuf` — пути,
  `CString`/`CStr` — нуль-терминированные строки для FFI, `Vec<u8>`/`&[u8]` —
  произвольные байты; переходы через `String::from_utf8` и
  `String::from_utf8_lossy`.
- **`Cow<'a, str>`** (clone-on-write) — «либо заимствовано, либо владеем»:
  подходит функциям вида «нормализуй строку, но не выделяй память, если
  менять нечего».
- **Сравнение и поиск**: `==` побайтовое, регистронезависимость —
  `eq_ignore_ascii_case` (только ASCII) или Unicode-крейт; `contains`,
  `starts_with`, `split`, `trim`, `replace`, `parse::<T>()` через трейт
  `FromStr`.
- **Что часто спрашивают**: почему `String` — это `Vec<u8>` с инвариантом
  UTF-8; чем `&String` хуже `&str` в сигнатуре (лишний уровень косвенности и
  сужение набора вызывающих); как работает deref coercion `String -> &str` и
  почему в обобщённом коде он не срабатывает без границы `AsRef<str>`.

## Ссылки

- [Book: Storing UTF-8 Encoded Text with Strings](https://doc.rust-lang.org/book/ch08-02-strings.html) — база и типичные ловушки.
- [std::string::String](https://doc.rust-lang.org/std/string/struct.String.html) — справочник по методам владеющей строки.
- [std::primitive::str](https://doc.rust-lang.org/std/primitive.str.html) — методы среза строки.
- [std::borrow::Cow](https://doc.rust-lang.org/std/borrow/enum.Cow.html) — clone-on-write в стандартной библиотеке.
- [std::ffi](https://doc.rust-lang.org/std/ffi/index.html) — `OsString`, `CString` и переходы между представлениями.
