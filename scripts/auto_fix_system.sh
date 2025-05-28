#!/bin/bash

# 改良版Bash構文エラー自動修正
auto_fix_bash_syntax_v2() {
    local file="$1"
    
    if ! bash -n "$file" 2>/dev/null; then
        echo "🔧 Bash構文エラー検出 - 自動修正試行中..."
        
        # 複数のバックアップパターンを試行
        for backup in "${file}_backup.sh" "${file}.backup" "${file%.*}_backup.sh"; do
            if [[ -f "$backup" ]]; then
                cp "$backup" "$file"
                echo "✅ バックアップから自動復旧完了: $backup"
                return 0
            fi
        done
        
        echo "❌ バックアップファイルが見つかりません"
        return 1
    else
        echo "✅ 構文エラーなし"
    fi
}

