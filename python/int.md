# int

[← Truthy and Falsy](truthy-falsy.md) · [🏠 Домой](../README.md) · [float →](float.md)

---

Тип для целых чисел (integer). Целые числа обладают негораниченной точностью (ограничена только доступной для процесса памятью)

Методы для int представленны в [документации](https://docs.python.org/3/library/stdtypes.html#additional-methods-on-integer-types)

`sys.set_int_max_str_digits()` (`python 3.11+`, security fix, бэкпортнут и в
3.9.14/3.10.7) — ограничивает длину строкового представления больших `int`
(по умолчанию 4300 цифр), защищая от DoS через `int(very_long_string)` /
`str(very_big_int)`, где сложность конвертации квадратичная.

---

[← Truthy and Falsy](truthy-falsy.md) · [🏠 Домой](../README.md) · [float →](float.md)
