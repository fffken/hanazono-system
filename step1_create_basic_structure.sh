#!/bin/bash
echo "🚀 段階1: HANAZONOシステム自動引き継ぎ基盤構築"
echo "⚠️ ステップバイステップで進行します"
echo ""

# 現在地確認
echo "📍 現在地確認"
pwd
echo ""

# 重要ファイル確認
echo "📁 重要ファイル確認:"
for file in "HANDOVER_PROMPT.md" "scripts/github_efficiency.sh" "email_notifier.py"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ⚠️ $file - 見つからず"
    fi
done
echo ""

echo "⏸️ 続行しますか？ Enter で続行"
read -p ""

read -p "続行しますか？ (Enter/Ctrl+C): "

# バックアップ作成
echo ""
echo "💾 バックアップ作成"
backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"

for file in "HANDOVER_PROMPT.md" "email_notifier.py" "main.py" "settings.json"; do
    if [ -f "$file" ]; then
        cp "$file" "$backup_dir/"
        echo "  ✅ $file → $backup_dir/"
    fi
done

echo "✅ バックアップ完了: $backup_dir"
echo ""

# ディレクトリ作成
echo "📁 ディレクトリ作成"
mkdir -p docs/navigation
mkdir -p scripts/auto_update
mkdir -p .claude

echo "✅ 完了"
echo "⏭️ 次: bash step1_create_files.sh"
