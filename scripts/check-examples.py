#!/usr/bin/env python3
"""Проверяет, что все примеры ```python в шпаргалке синтаксически корректны.

Ловит опечатки, поехавшие отступы и неполные конструкции в кодовых блоках —
то есть примеры, которые читатель не сможет скопировать и запустить.

Блоки в шпаргалке часто фрагментарны (без объемлющей функции, с `return` или
`async with` на верхнем уровне), поэтому проверка идёт в три попытки:
  1. как есть;
  2. после снятия общего отступа;
  3. обёрнутым в `async def`, что легализует return/await/async with.
Блок считается сломанным, только если не прошла ни одна попытка.

Если пример должен демонстрировать НЕВАЛИДНЫЙ код, пометьте блок как ```text —
такие блоки не проверяются.

Запуск: python scripts/check-examples.py
Код возврата: 0 — чисто, 1 — есть сломанные блоки.
"""
from __future__ import annotations

import pathlib
import re
import sys
import textwrap

DIRS = ("fundamentals", "python", "sql", "topics")
BLOCK = re.compile(r"```python\n(.*?)```", re.DOTALL)


def compiles(code: str) -> bool:
    try:
        compile(code, "<block>", "exec")
    except SyntaxError:
        return False
    return True


def check_block(code: str) -> str | None:
    """Возвращает сообщение об ошибке или None, если блок в порядке."""
    if compiles(code):
        return None

    dedented = textwrap.dedent(code)
    if compiles(dedented):
        return None

    wrapped = "async def _wrapper():\n" + textwrap.indent(dedented, "    ")
    if compiles(wrapped):
        return None

    try:
        compile(dedented, "<block>", "exec")
    except SyntaxError as exc:
        where = f" (строка блока {exc.lineno})" if exc.lineno else ""
        return f"{exc.msg}{where}: {(exc.text or '').strip()[:70]}"
    return "не компилируется"


def check_file(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    problems = []

    for match in BLOCK.finditer(text):
        problem = check_block(match.group(1))
        if problem:
            line = text[: match.start()].count("\n") + 1
            problems.append(f"{path}:{line}: {problem}")

    return problems


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    problems: list[str] = []
    total = 0

    for directory in DIRS:
        for path in sorted((root / directory).glob("*.md")):
            text = path.read_text(encoding="utf-8")
            total += len(BLOCK.findall(text))
            problems.extend(check_file(path.relative_to(root)))

    if problems:
        print("\n".join(problems))
        print(f"\nсломанных блоков: {len(problems)} из {total}")
        return 1

    print(f"OK: все {total} python-примеров синтаксически корректны")
    return 0


if __name__ == "__main__":
    sys.exit(main())
