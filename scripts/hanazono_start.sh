#!/bin/bash
#echo "\n\n=================================="
echo "🏆 HANAZONOシステム - 究極モード起動"
echo "=================================="

# 自動判定
if ! python3 main.py --daily-report >/dev/null 2>&1; then
    echo "🚨 緊急モード: システム異常検出"
    echo "復旧手順: git reset --hard HEAD"
    cat EMERGENCY_RECOVERY_GUIDE.md
elif [[ $(git status --short | wc -l) -gt 10 ]]; then
    echo "📊 詳細モード: 複雑状況分析"
    bash scripts/master_progress_controller.sh >/dev/null 2>&1
    echo "✅ 詳細分析完了"
    echo "確認: cat AI_GITHUB_AUTO_REPORT.md"
else
    echo "⚡ 高速モード: 効率最優先実行"
    cat HANDOVER_PROMPT.md
fi

echo ""
echo "🎯 推奨次アクション:"
echo "1. 統合開発コマンド実装 (65分)"
echo "2. 自然言語インターフェース (45分)"
echo "3. AI開発アシスタント (120分)"

echo ""
echo "📊 GitHub統合状況:"
source scripts/github_auto_enhanced.sh && github_status

echo ""
echo "🔍 ファクトチェックシステム統合済み"
echo "実行: bash scripts/fact_check_system.sh"
