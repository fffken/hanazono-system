#!/bin/bash
# GitHub Raw URL生成スクリプト（シンプル版）

REPO_URL=$(git config --get remote.origin.url | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')
BRANCH=$(git branch --show-current)

echo "# HANAZONOシステム 重要ファイル直接リンク"
echo ""
echo "## コードファイル"
for file in main.py email_notifier.py settings_manager.py; do
  if [ -f "$file" ]; then
    raw_url="${REPO_URL}/raw/${BRANCH}/${file}"
    echo "- [$file]($raw_url)"
  fi
done

echo ""
echo "## ドキュメント"
for doc in docs/*.md; do
  if [ -f "$doc" ]; then
    raw_url="${REPO_URL}/raw/${BRANCH}/${doc}"
    echo "- [$(basename $doc)]($raw_url)"
  fi
done

echo ""
echo "## 引き継ぎリソース"
echo "- [プロジェクト状態](${REPO_URL}/raw/${BRANCH}/PROJECT_STATUS.md)"
echo "- [引き継ぎ情報](${REPO_URL}/raw/${BRANCH}/PROJECT_HANDOVER.md)"
echo ""
