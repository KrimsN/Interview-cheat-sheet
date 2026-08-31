# DDL / DML / DCL / TCL и базовые команды

[← СУБД, таблицы, сущности](dbms-basics.md) · [🏠 Домой](../README.md) · [Типы данных →](data-types.md)

---

## Из каких подмножеств состоит SQL?

**Коротко.** Четыре основных: DDL (структура), DML (данные), DCL (права),
TCL (транзакции). Иногда `SELECT` выделяют отдельно как DQL.

| Подмножество | Что делает | Команды |
|---|---|---|
| **DDL** — Data Definition Language | Описывает структуру | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` |
| **DML** — Data Manipulation Language | Меняет данные | `INSERT`, `UPDATE`, `DELETE`, `MERGE` |
| **DQL** — Data Query Language | Читает данные | `SELECT` |
| **DCL** — Data Control Language | Управляет правами | `GRANT`, `REVOKE` |
| **TCL** — Transaction Control Language | Управляет транзакциями | `COMMIT`, `ROLLBACK`, `SAVEPOINT` |

**Подвох.** Ответ без **TCL** засчитают как неполный — именно транзакции обычно
и есть то, к чему интервьюер ведёт следующим вопросом.

---

## В чём разница между `DELETE`, `TRUNCATE` и `DROP`?

**Коротко.** `DELETE` удаляет строки построчно и может иметь `WHERE`;
`TRUNCATE` мгновенно очищает всю таблицу; `DROP` удаляет саму таблицу вместе со
структурой.

| | DELETE | TRUNCATE | DROP |
|---|---|---|---|
| Что удаляет | строки | все строки | таблицу целиком |
| Поддерживает `WHERE` | да | нет | — |
| Подмножество | DML | DDL | DDL |
| Скорость на большой таблице | медленно | быстро | быстро |
| Вызывает триггеры на строки | да | нет | — |

`TRUNCATE` быстрее, потому что не удаляет строки по одной и не пишет их все в
журнал — он просто освобождает страницы данных.

**Подвох.** Утверждение «после `DELETE` данные можно восстановить, а после
`TRUNCATE` нельзя» — неверно. Восстановимость зависит не от команды, а от того,
закоммичена ли транзакция:

- **PostgreSQL** — DDL транзакционен. И `TRUNCATE`, и даже `DROP TABLE` внутри
  `BEGIN ... ROLLBACK` откатываются полностью.
- **MySQL** — DDL-команды вызывают неявный `COMMIT`, поэтому откатить
  `TRUNCATE` или `DROP` нельзя ни при каких условиях.
- После `COMMIT` в любой СУБД ни то, ни другое средствами SQL не вернуть —
  только из резервной копии.

```sql
-- PostgreSQL
BEGIN;
DROP TABLE orders;
ROLLBACK;      -- таблица на месте
```

**Глубже.** В PostgreSQL `TRUNCATE` по умолчанию **не сбрасывает** счётчики
последовательностей — для этого нужно `TRUNCATE ... RESTART IDENTITY`. Это
частое заблуждение.

---

## Как получить текущую дату?

**Коротко.** По стандарту — `CURRENT_DATE` и `CURRENT_TIMESTAMP`. Они работают
и в PostgreSQL, и в MySQL.

```sql
SELECT CURRENT_DATE;        -- стандарт SQL
SELECT CURRENT_TIMESTAMP;   -- стандарт SQL

SELECT now();               -- PostgreSQL
SELECT NOW();               -- MySQL
SELECT GETDATE();           -- только MS SQL Server (T-SQL)
```

**Подвох.** `GETDATE()` — функция T-SQL, а не «встроенная функция SQL». В
PostgreSQL и MySQL она не существует, вызов упадёт с ошибкой. Безопасный ответ
на собеседовании — `CURRENT_TIMESTAMP`.

---

## Как выбрать только уникальные значения?

```sql
SELECT DISTINCT name FROM users;
```

`DISTINCT` убирает дубликаты по всем перечисленным столбцам сразу, а не по
каждому отдельно: `SELECT DISTINCT city, name` вернёт уникальные **пары**.

**Глубже.** В PostgreSQL есть `DISTINCT ON (col)` — вернуть по одной строке на
каждое значение `col`, выбрав какую именно через `ORDER BY`. Это расширение
Postgres, в стандарте его нет.

---

## Как вставить строку или обновить её, если она уже есть (upsert)?

```sql
-- PostgreSQL
INSERT INTO users (id, name) VALUES (1, 'Анна')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;

-- MySQL
INSERT INTO users (id, name) VALUES (1, 'Анна')
ON DUPLICATE KEY UPDATE name = VALUES(name);
```

`ON CONFLICT ... DO NOTHING` — вариант «вставить, если ещё нет, и молча пройти
мимо, если есть».

---

[← СУБД, таблицы, сущности](dbms-basics.md) · [🏠 Домой](../README.md) · [Типы данных →](data-types.md)
