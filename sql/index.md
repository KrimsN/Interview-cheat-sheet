# SQL — вопросы и ответы для собеседований

[🏠 Домой](../README.md) · [СУБД, таблицы, сущности →](dbms-basics.md)

---

Темы в порядке чтения. Примеры ориентированы на **PostgreSQL** как основную СУБД;
там, где MySQL или MS SQL Server ведут себя иначе, это отмечено явно.

1. [СУБД, таблицы, сущности и отношения](dbms-basics.md) — виды СУБД, связи 1:1, 1:N, M:N
2. [DDL/DML/DCL/TCL и базовые команды](ddl-dml-dcl.md) — DELETE vs TRUNCATE vs DROP, upsert
3. [Типы данных](data-types.md) — CHAR vs VARCHAR, числа и деньги, `timestamptz`, `JSONB`
4. [Ключи и ограничения](keys-constraints.md) — PK/UNIQUE/FK, `ON DELETE`, целостность
5. [JOIN](joins.md) — виды соединений, `ON` vs `WHERE`, self join, `NOT IN` с `NULL`
6. [Индексы](indexes.md) — B-tree/GIN/BRIN, составные индексы, `EXPLAIN`
7. [Нормализация и денормализация](normalization.md) — 1NF-3NF, BCNF, аномалии
8. [ACID, изоляция транзакций и NULL](acid-and-null.md) — уровни изоляции, MVCC, трёхзначная логика
9. [Внешние ссылки](references.md)

---

[🏠 Домой](../README.md) · [СУБД, таблицы, сущности →](dbms-basics.md)
