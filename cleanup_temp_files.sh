#!/bin/bash
echo "🤖 AI推奨による一時ファイル自動クリーンアップ"

# 修正作業用ファイルを自動削除
rm -f fix*.py
rm -f tiny_fix*.py
rm -f simple_fix.py
rm -f safe_fix.py

# バックアップファイルをバックアップディレクトリに移動
mkdir -p old_backups
mv *.bak old_backups/ 2>/dev/null
mv *.orig old_backups/ 2>/dev/null

echo "✅ 一時ファイル自動クリーンアップ完了"
