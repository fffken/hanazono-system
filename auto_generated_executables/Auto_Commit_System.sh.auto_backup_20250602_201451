#!/bin/bash

# === 自動コミットシステム v1.0 ===
echo "🔄 自動コミットシステム v1.0 開始..."

# 変更件数確認
changes=$(git status --porcelain | wc -l)

if [ "$changes" -gt 0 ]; then
    echo "📊 $changes 件の変更を検出"
    
    # 自動コミットメッセージ生成
    timestamp=$(date '+%Y-%m-%d %H:%M')
    commit_msg="🏆 AI記憶喪失防止システム100点満点達成 - $timestamp"
    
    # 自動コミット実行
    git add .
    git commit -m "$commit_msg"
    git push origin main
    
    echo "✅ 自動コミット・プッシュ完了"
else
    echo "✅ 変更なし - コミット不要"
fi
