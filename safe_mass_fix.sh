#!/bin/bash
# メール機能保護付き安全修復
while read file; do
    if [[ "$file" != *"email_protection_vault"* ]] && [[ "$file" != *"GOLDEN_MASTER"* ]]; then
        echo "修復中: $file"
        cp "$file" "${file}.broken_backup" 2>/dev/null
        sed 's/)$//' "$file" > "${file}.temp" 2>/dev/null
        if python3 -m py_compile "${file}.temp" 2>/dev/null; then
            mv "${file}.temp" "$file"
            echo "✅ 修復完了: $file"
        else
            echo "❌ 修復失敗: $file"
            rm "${file}.temp" 2>/dev/null
        fi
    fi
done < broken_files_list.txt
