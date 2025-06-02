#!/bin/bash
# HANAZONOシステム 状態確認スクリプト

echo "=== HANAZONOシステム 状態確認 $(date) ==="

echo "## Git状態"
git status --short

echo "## 最新コミット"
git log -n 3 --oneline

echo "## コアファイル"
echo "1. main.py: $(head -n 1 main.py | cut -c 3-)"
echo "2. email_notifier.py: $(grep -n "class EmailNotifier" email_notifier.py | head -n 1)"
echo "3. lvyuan_collector.py: $(grep -n "class LvyuanCollector" lvyuan_collector.py 2>/dev/null || echo "未検出")"
echo "4. settings_manager.py: $(grep -n "class SettingsManager" settings_manager.py 2>/dev/null || echo "未検出")"

echo "## メール通知状態"
grep -n "def send_daily_report" email_notifier.py | head -n 1

echo "## 未解決の課題"
if [ -f "PROJECT_STATUS.md" ]; then
  cat PROJECT_STATUS.md | grep -A 5 "次のアクション"
else
  echo "PROJECT_STATUS.md ファイルが見つかりません"
fi

echo "## バックアップ状況"
find backups -type f -name "email_notifier*" | wc -l

