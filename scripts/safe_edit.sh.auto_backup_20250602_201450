#!/bin/bash
safe_edit() {
    local file="$1"
    local backup="${file}.backup"
    cp "$file" "$backup"
    shift; "$@"
    if python3 -m py_compile "$file" 2>/dev/null; then
        rm "$backup"; echo "✅ 編集成功"
    else
        cp "$backup" "$file"; rm "$backup"; echo "❌ 復旧完了"
    fi
}
