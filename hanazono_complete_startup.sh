#!/bin/bash
# HANAZONO完全統合起動システム v1.0
# 新AIセッション開始時の完全自動化

echo "🚀 HANAZONO AI EMPIRE 完全起動開始..."
echo "========================================"

# 1. GitHub自動読み込み
echo "📥 GitHub重要ファイル取得中..."
./fetch_github_files.sh fetch_all

# 2. 取得したファイル内容を表示
echo ""
echo "📋 AI作業ルール確認:"
echo "===================="
if [ -f "github_files/AI_WORK_RULES.md" ]; then
    head -20 github_files/AI_WORK_RULES.md
    echo "... (続きは github_files/AI_WORK_RULES.md を参照)"
else
    echo "❌ AI_WORK_RULES.md が見つかりません"
fi

echo ""
echo "📊 プロジェクト状況確認:"
echo "========================"
if [ -f "github_files/PROJECT_STATUS.md" ]; then
    head -20 github_files/PROJECT_STATUS.md
    echo "... (続きは github_files/PROJECT_STATUS.md を参照)"
else
    echo "❌ PROJECT_STATUS.md が見つかりません"
fi

echo ""
echo "🔄 自動引き継ぎ情報:"
echo "==================="
if [ -f "github_files/github_auto_handover.md" ]; then
    head -20 github_files/github_auto_handover.md
    echo "... (続きは github_files/github_auto_handover.md を参照)"
else
    echo "❌ github_auto_handover.md が見つかりません"
fi

# 3. システム状態確認
echo ""
echo "🏛️ AI帝国状態確認:"
echo "=================="
if [ -f "empire_dashboard.sh" ]; then
    bash empire_dashboard.sh
else
    echo "❌ empire_dashboard.sh が見つかりません"
fi

# 4. 利用可能コマンド表示
echo ""
echo "🔧 利用可能コマンド:"
echo "=================="
echo "h 'システム状態確認'    # 統合システム確認"
echo "ai 'バグ修正して'        # AI自動開発"
echo "dashboard               # リアルタイム監視画面"
echo "hanazono detail         # 詳細情報確認"
echo "bash scripts/auto_git_organize_push.sh  # Git自動整理"

# 5. 現在のシステム状況
echo ""
echo "📊 現在のシステム状況:"
echo "===================="
echo "📅 起動時刻: $(date)"
echo "💻 ホスト名: $(hostname)"
echo "📁 作業ディレクトリ: $(pwd)"
echo "🔧 Pythonプロセス数: $(ps aux | grep python3 | grep -v grep | wc -l)"

echo ""
echo "✅ HANAZONO AI EMPIRE 完全起動完了！"
echo "========================================"
echo "🎯 新AIセッション準備完了 - 作業を開始できます！"
