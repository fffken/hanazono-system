#!/bin/bash

# 自動コミットメッセージ生成（強化版）
auto_commit() {
    local changes=$(git status --short | wc -l)
    local added=$(git status --short | grep "^A" | wc -l)
    local modified=$(git status --short | grep "^M" | wc -l)
    local deleted=$(git status --short | grep "^D" | wc -l)
    
    local message=""
    if [[ $changes -gt 15 ]]; then
        message="🔧 大規模システム更新"
    elif [[ $changes -gt 5 ]]; then
        message="🚀 開発進捗保存"
    else
        message="✨ 軽微な改善"
    fi
    
    message="$message - $(date '+%Y-%m-%d %H:%M:%S')"
    message="$message (追加:$added 変更:$modified 削除:$deleted)"
    
    git add . && git commit -m "$message" && git push
    echo "✅ 自動コミット完了: $message"
}

# GitHub情報統合表示
github_status() {
    echo "📊 GitHub統合状況:"
    echo "  現在ブランチ: $(git branch --show-current)"
    echo "  未コミット: $(git status --short | wc -l)件"
    echo "  最新コミット: $(git log -1 --oneline)"
}
