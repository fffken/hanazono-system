#!/bin/bash

# GitHub Personal Access Token
TOKEN="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"

# ファイルを取得して表示する関数
fetch_github_file() {
  local repo="$1"
  local path="$2"
  
  echo "=== 取得中: $path ==="
  curl -s -H "Authorization: token $TOKEN" \
    "https://raw.githubusercontent.com/$repo/main/$path"
  
  echo -e "\n\n=== $path の取得完了 ===\n"
}

# メイン処理
echo "HANAZONOシステム AI用ドキュメント取得ツール"
echo "================================================"

# 指定されたファイルを取得
if [ "$1" != "" ]; then
  fetch_github_file "fffken/hanazono-system" "$1"
  exit 0
fi

# ファイルが指定されていない場合、デフォルトの重要ファイルを取得
echo "重要なドキュメントを取得しています..."

# CLAUDE_START_HERE.md を取得
fetch_github_file "fffken/hanazono-system" "docs/navigation/CLAUDE_START_HERE.md"

# 他の重要ファイルも取得可能
# fetch_github_file "fffken/hanazono-system" "docs/HANDOVER_COMPLETE.md"
# fetch_github_file "fffken/hanazono-system" "docs/project/progress_log.md"

echo "ドキュメント取得が完了しました。"
