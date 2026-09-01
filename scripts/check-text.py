#!/usr/bin/env python3
"""Проверяет markdown-файлы шпаргалки на текстовые дефекты.

Что ловит:
  1. Смешанную раскладку внутри слова (латиница + кириллица) — например
     "molча", "menять". Глазами такое почти не видно.
  2. Посторонние системы письма (CJK, греческий) — залетают при генерации.
  3. Известные опечатки из списка.

Запуск: python scripts/check-text.py
Код возврата: 0 — чисто, 1 — есть находки.
"""
from __future__ import annotations

import pathlib
import re
import sys
import unicodedata

DIRS = ("fundamentals", "python", "sql", "topics")

# Опечатки, найденные при ревизии. Ключ — регулярное выражение, значение — как надо.
TYPOS = {
    r"обьект": "объект",
    r"негораниченн": "неограниченн",
    r"интерпритатор": "интерпретатор",
    r"при передачи\b": "при передаче",
    r"в качетве": "в качестве",
    r"длинну": "длину",
    r"отличае\b": "отличие",
    r"обратботает": "обработает",
    r"реализованны\b": "реализованы",
    r"представленны\b": "представлены",
    r"соеденение": "соединение",
    r"произведенинем": "произведением",
    r"стблиц": "таблиц",
    r"comperhantion": "comprehension",
    r"\bлуче\b": "лучше",
}

CYRILLIC = re.compile(r"[а-яёА-ЯЁ]")
LATIN = re.compile(r"[a-zA-Z]")
# слово целиком, без разрывов
WORD = re.compile(r"[a-zA-Zа-яёА-ЯЁ]{2,}")


def allowed_codepoint(ch: str) -> bool:
    """Разрешены ASCII, кириллица, типографика, стрелки, рамки и эмодзи."""
    o = ord(ch)
    if o < 0x0500:  # ASCII + кириллица
        return True
    if 0x2000 <= o <= 0x27BF:  # пунктуация, стрелки, рамки, символы
        return True
    if 0x2B00 <= o <= 0x2BFF or o in (0xFE0F, 0x200D):
        return True
    if 0x1F000 <= o <= 0x1FAFF:  # эмодзи
        return True
    return False


def strip_code_spans(line: str) -> str:
    """Убирает `код` — там смешение раскладок легально (например `id`)."""
    return re.sub(r"`[^`]*`", " ", line)


def check_file(path: pathlib.Path) -> list[str]:
    found: list[str] = []
    in_fence = False

    for num, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue

        # посторонние системы письма проверяем даже в коде
        for ch in raw:
            if not allowed_codepoint(ch):
                name = unicodedata.name(ch, "неизвестный символ")
                found.append(f"{path}:{num}: посторонний символ U+{ord(ch):04X} ({name})")

        if in_fence:
            continue

        text = strip_code_spans(raw)

        for word in WORD.findall(text):
            if CYRILLIC.search(word) and LATIN.search(word):
                found.append(f"{path}:{num}: смешанная раскладка в слове {word!r}")

        for pattern, correct in TYPOS.items():
            if re.search(pattern, text, re.IGNORECASE):
                found.append(f"{path}:{num}: опечатка {pattern!r} -> надо {correct!r}")

    return found


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    problems: list[str] = []

    for directory in DIRS:
        for path in sorted((root / directory).glob("*.md")):
            problems.extend(check_file(path.relative_to(root)))

    if problems:
        print("\n".join(problems))
        print(f"\nнайдено проблем: {len(problems)}")
        return 1

    print("OK: текстовых дефектов не найдено")
    return 0


if __name__ == "__main__":
    sys.exit(main())
