#!/bin/bash
# Auto-Generated Executable
# Task: GitHub_API_Complete_System_v5
# Description: GitHub API完全活用システム v5.0 - v4.0同等の完璧な基盤システム
# Generated: Sat 24 May 20:30:10 JST 2025

set -e
echo "🚀 実行開始: GitHub_API_Complete_System_v5"
echo "📝 説明: GitHub API完全活用システム v5.0 - v4.0同等の完璧な基盤システム"
echo ""


# === GitHub API完全活用システム v5.0 ===
echo "🔍 GitHub API完全解析開始..."

# GitHub API認証確認
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN が設定されていません"
    exit 1
fi

echo "✅ GitHub認証確認完了"


# リポジトリ完全解析
echo "📊 リポジトリ完全解析中..."
REPO_INFO=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
    "https://api.github.com/repos/$GITHUB_REPO")

echo "✅ リポジトリ情報取得完了"


# === GitHub API完全活用システム v5.0 ===
echo "🔍 GitHub API完全解析開始..."

# GitHub API認証確認
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN が設定されていません"
    exit 1
fi

echo "✅ GitHub認証確認完了"
REPO="$GITHUB_REPO"
API_BASE="https://api.github.com/repos/$REPO"

# レポートファイル初期化
REPORT_FILE="GITHUB_API_COMPLETE_REPORT_v5.md"
echo "# GitHub API完全活用システム v5.0 レポート" > $REPORT_FILE
echo "**生成時刻**: $(date)" >> $REPORT_FILE
echo "**リポジトリ**: $REPO" >> $REPORT_FILE
echo "" >> $REPORT_FILE

echo "📊 リポジトリ完全解析中..."

# リポジトリ基本情報
REPO_INFO=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" "$API_BASE")
echo "## 📊 リポジトリ基本情報" >> $REPORT_FILE
echo "- **名前**: $(echo $REPO_INFO | jq -r '.name // "N/A"')" >> $REPORT_FILE
echo "- **説明**: $(echo $REPO_INFO | jq -r '.description // "N/A"')" >> $REPORT_FILE
echo "- **言語**: $(echo $REPO_INFO | jq -r '.language // "N/A"')" >> $REPORT_FILE
echo "- **スター数**: $(echo $REPO_INFO | jq -r '.stargazers_count // "N/A"')" >> $REPORT_FILE
echo "- **フォーク数**: $(echo $REPO_INFO | jq -r '.forks_count // "N/A"')" >> $REPORT_FILE
echo "- **最終更新**: $(echo $REPO_INFO | jq -r '.updated_at // "N/A"')" >> $REPORT_FILE
echo "" >> $REPORT_FILE

echo "✅ リポジトリ基本情報取得完了"

echo "📝 コミット履歴完全分析中..."

# 最新コミット情報
COMMITS=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" "$API_BASE/commits?per_page=10")
echo "## 📝 最新コミット履歴（10件）" >> $REPORT_FILE
echo "$COMMITS" | jq -r '.[] | "- **\(.commit.message | split("\n")[0])** - \(.commit.author.name) (\(.commit.author.date))"' >> $REPORT_FILE
echo "" >> $REPORT_FILE

# コミット統計
COMMIT_COUNT=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" "$API_BASE/commits" | jq '. | length')
echo "## 📊 コミット統計" >> $REPORT_FILE
echo "- **総コミット数**: $COMMIT_COUNT" >> $REPORT_FILE
echo "" >> $REPORT_FILE

echo "✅ コミット履歴分析完了"

echo "🌿 ブランチ・タグ分析中..."

# ブランチ情報
BRANCHES=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" "$API_BASE/branches")
echo "## 🌿 ブランチ情報" >> $REPORT_FILE
echo "$BRANCHES" | jq -r '.[] | "- **\(.name)** - 最終コミット: \(.commit.sha[0:7])"' >> $REPORT_FILE
echo "" >> $REPORT_FILE

# タグ情報
TAGS=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" "$API_BASE/tags?per_page=5")
echo "## 🏷️ 最新タグ（5件）" >> $REPORT_FILE
echo "$TAGS" | jq -r '.[] | "- **\(.name)** - \(.commit.sha[0:7])"' >> $REPORT_FILE
echo "" >> $REPORT_FILE

echo "✅ ブランチ・タグ分析完了"

echo "🎯 Issue/PR完全分析中..."

# オープンIssue
OPEN_ISSUES=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" "$API_BASE/issues?state=open&per_page=10")
echo "## 🎯 オープンIssue（10件）" >> $REPORT_FILE
if [ "$(echo $OPEN_ISSUES | jq '. | length')" -gt 0 ]; then
    echo "$OPEN_ISSUES" | jq -r '.[] | "- **#\(.number)** \(.title) - \(.user.login) (\(.created_at))"' >> $REPORT_FILE
else
    echo "- オープンなIssueはありません" >> $REPORT_FILE
fi
echo "" >> $REPORT_FILE

# プルリクエスト
PULL_REQUESTS=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" "$API_BASE/pulls?state=open&per_page=5")
echo "## 🔄 オープンプルリクエスト（5件）" >> $REPORT_FILE
if [ "$(echo $PULL_REQUESTS | jq '. | length')" -gt 0 ]; then
    echo "$PULL_REQUESTS" | jq -r '.[] | "- **#\(.number)** \(.title) - \(.user.login) (\(.created_at))"' >> $REPORT_FILE
else
    echo "- オープンなプルリクエストはありません" >> $REPORT_FILE
fi
echo "" >> $REPORT_FILE

echo "✅ Issue/PR分析完了"

echo "📋 最終レポート生成中..."

# GitHub API使用状況
RATE_LIMIT=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" "https://api.github.com/rate_limit")
echo "## 📊 GitHub API使用状況" >> $REPORT_FILE
echo "- **残り回数**: $(echo $RATE_LIMIT | jq -r '.rate.remaining')/$(echo $RATE_LIMIT | jq -r '.rate.limit')" >> $REPORT_FILE
echo "- **リセット時刻**: $(date -d @$(echo $RATE_LIMIT | jq -r '.rate.reset'))" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# 完了メッセージ
echo "## 🎉 GitHub API完全活用システム v5.0 完了" >> $REPORT_FILE
echo "- **解析完了時刻**: $(date)" >> $REPORT_FILE
echo "- **レポートファイル**: $REPORT_FILE" >> $REPORT_FILE

echo "🎉 GitHub API完全活用システム v5.0 完了！"
echo "📋 詳細レポート: $REPORT_FILE"
echo ""
echo "📊 レポート確認方法:"
echo "cat $REPORT_FILE"
