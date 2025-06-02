#!/bin/bash
# 空の例外処理修正スクリプト

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}=== 空の例外処理修正ツール ===${NC}"

# 重要ファイルのリスト
IMPORTANT_FILES=(
    "main.py"
    "email_notifier.py"
    "settings_manager.py"
    "lvyuan_collector.py"
    "data_util.py"
)

fix_empty_except() {
    local file="$1"
    local backup_file="${file}.backup_$(date +%Y%m%d_%H%M%S)"
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}ファイルが見つかりません: $file${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}修正中: $file${NC}"
    
    # バックアップ作成
    cp "$file" "$backup_file"
    echo "  📁 バックアップ作成: $backup_file"
    
    # 空の例外処理を検出して修正提案を表示
    python3 -c "
import re
import sys

with open('$file', 'r', encoding='utf-8') as f:
    lines = f.readlines()

modified_lines = []
changes_made = 0

for i, line in enumerate(lines):
    # 空の例外処理パターンを検出
    if re.match(r'^\s*except.*:\s*$', line):
        # 次の行が空または pass の場合
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line == '' or next_line == 'pass':
                # より適切な例外処理に置換
                indent = len(line) - len(line.lstrip())
                new_except = line.rstrip() + '\n'
                new_pass = ' ' * (indent + 4) + 'logging.warning(f\"Exception occurred: {e}\")\n'
                new_pass += ' ' * (indent + 4) + 'pass\n'
                
                modified_lines.append(new_except)
                modified_lines.append(new_pass)
                changes_made += 1
                
                # 元の pass 行をスキップ
                if i + 1 < len(lines) and lines[i + 1].strip() == 'pass':
                    continue
                continue
    
    modified_lines.append(line)

# ファイルに書き戻し
if changes_made > 0:
    with open('$file', 'w', encoding='utf-8') as f:
        f.writelines(modified_lines)
    print(f'  ✅ {changes_made}件の空の例外処理を修正しました')
else:
    print('  ℹ️  修正が必要な空の例外処理は見つかりませんでした')
"
}

# メイン実行
main() {
    # logging import の確認・追加
    for file in "${IMPORTANT_FILES[@]}"; do
        if [ -f "$file" ]; then
            # logging import が存在するかチェック
            if ! grep -q "import logging" "$file"; then
                echo -e "${YELLOW}$file に logging import を追加します${NC}"
                # ファイルの先頭付近に logging import を追加
                sed -i '1i import logging' "$file"
                echo "  ✅ logging import を追加しました"
            fi
            
            # 例外処理を修正
            fix_empty_except "$file"
            echo ""
        else
            echo -e "${RED}ファイルが見つかりません: $file${NC}"
        fi
    done
    
    echo -e "${GREEN}=== 修正完了 ===${NC}"
    echo "修正されたファイルの動作確認を行ってください："
    echo "  python3 -m py_compile main.py"
    echo "  python3 -m py_compile email_notifier.py"
}

main "$@"
