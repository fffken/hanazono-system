#!/bin/bash
echo "=== HANAZONOシステム AI完全引き継ぎ ==="
echo "実行日時: $(date)"
echo ""

# 1. GitHub設定確認
echo "【1. GitHub設定状況】"
bash scripts/setup_github.sh
echo ""

# 2. プロジェクト状況確認
echo "【2. プロジェクト状況】"
bash scripts/github_efficiency.sh
echo ""

# 3. システム健全性確認
echo "【3. システム健全性】"
python3 -c "
from system_health_monitor import SystemHealthMonitor
monitor = SystemHealthMonitor()
health = monitor.comprehensive_health_check()
print(f'総合ステータス: {health[\"overall_status\"].upper()}')
for check, result in health['checks'].items():
    emoji = '✅' if result['status'] else '❌'
    print(f'{emoji} {check}: {result[\"message\"]}')
"
echo ""

# 4. GitHub API動作確認
echo "【5. GitHubトークン状況】"
echo "トークン: HANAZONOシステム用"
echo "有効期限: 2025年8月19日"
if command -v gh >/dev/null 2>&1; then
    echo "状態: $(gh auth status 2>/dev/null && echo '有効' || echo '要確認')"
else
    echo "状態: gh CLI未インストール - Python APIで確認中"
fi
echo ""
echo "【4. GitHub API動作確認】"
python3 -c "
from github_auto_fetch import GitHubAutoFetch
try:
    fetcher = GitHubAutoFetch()
    files = fetcher.get_file_list()
    if files:
        print('✅ GitHub API正常動作')
        print(f'ファイル数: {len(files)}件')
    else:
        print('❌ GitHub API接続エラー')
except Exception as e:
    print(f'❌ GitHub API エラー: {e}')
"


echo "【6. プロジェクト理解確認】"
if [ -f "PROJECT_UNDERSTANDING.md" ]; then
    echo "✅ プロジェクト理解文書存在"
    echo "📋 メール機能要件: 表示順序6項目確定"
    echo "🎯 目標: 年間20万円削減、設定半自動化"
    echo "⚙️ 重要パラメータ: ID 07,10,62の最適化"
else
    echo "❌ プロジェクト理解文書が必要"
fi
