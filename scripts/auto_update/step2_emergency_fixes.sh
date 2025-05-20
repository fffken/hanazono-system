#!/bin/bash
# step2_emergency_fixes.sh - 緊急修正実行

echo "🚨 緊急修正実行"
echo "==================="

# バックアップ作成
backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"
for file in "settings.json" "main.py"; do
    if [ -f "$file" ]; then
        cp "$file" "$backup_dir/"
        echo "  ✅ $file → $backup_dir/"
    fi
done

# settings.json 修正
if [ -f "settings.json" ]; then
    echo "settings.json修正中..."
    python3 -c "
import json
with open('settings.json', 'r') as f:
    data = json.load(f)
if 'email' in data:
    removed = []
    if 'email_address' in data['email']:
        data['email'].pop('email_address')
        removed.append('email_address')
    if 'email_password' in data['email']:
        data['email'].pop('email_password')
        removed.append('email_password')
    if removed:
        with open('settings.json', 'w') as f:
            json.dump(data, f, indent=2)
        print('✅ 重複削除: ' + ', '.join(removed))
    else:
        print('ℹ️ 重複なし')
"
fi

# main.py 修正確認
if [ -f "main.py" ]; then
    echo "main.py確認中..."
    echo "重複箇所がある場合は手動で修正してください"
    grep -n "settings_manager" main.py | head -3
    grep -n "json.load" main.py | head -3
fi

echo "✅ 緊急修正完了"
echo "バックアップ: $backup_dir"
