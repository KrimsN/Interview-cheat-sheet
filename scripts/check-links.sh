#!/usr/bin/env bash
# Проверяет относительные markdown-ссылки в python/ и sql/:
# - что каждая ссылка вида ](file.md) или ](file.md#anchor) указывает на
#   существующий файл;
# - что на каждый .md-файл раздела (кроме index.md) есть хотя бы одна
#   входящая ссылка — иначе он выпал из цепочки навигации.
#
# Запуск: bash scripts/check-links.sh
# Код возврата: 0 — всё чисто, 1 — есть проблемы (см. вывод).

set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

status=0
tmp_linked="$(mktemp)"
trap 'rm -f "$tmp_linked"' EXIT

check_dir() {
    local dir="$1" file filedir link target resolved resolveddir base
    [ -d "$dir" ] || return 0

    while IFS= read -r file; do
        filedir=$(dirname "$file")
        while IFS= read -r link; do
            [ -z "$link" ] && continue
            target=${link%%#*}
            [ -z "$target" ] && continue
            resolved="$filedir/$target"
            base=$(basename "$resolved")
            resolveddir=$(cd "$(dirname "$resolved")" 2>/dev/null && pwd) || resolveddir=""
            if [ -z "$resolveddir" ] || [ ! -f "$resolveddir/$base" ]; then
                echo "BROKEN LINK: $file -> $link"
                status=1
            else
                echo "$resolveddir/$base" >> "$tmp_linked"
            fi
        done < <(grep -oE '\]\([^)]+\.md(#[^)]*)?\)' "$file" | sed -E 's/^\]\((.*)\)$/\1/')
    done < <(find "$dir" -name '*.md')
}

check_dir python
check_dir sql

echo "--- файлы без входящих ссылок (кроме index.md) ---"
for dir in python sql; do
    [ -d "$dir" ] || continue
    while IFS= read -r file; do
        abs="$(cd "$(dirname "$file")" && pwd)/$(basename "$file")"
        if ! grep -qxF "$abs" "$tmp_linked" 2>/dev/null; then
            echo "ORPHAN (нет входящих ссылок): $file"
            status=1
        fi
    done < <(find "$dir" -name '*.md' ! -name 'index.md')
done

[ "$status" -eq 0 ] && echo "OK: битых ссылок и сирот не найдено"

exit "$status"
