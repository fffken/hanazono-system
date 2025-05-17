#!/bin/bash
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
echo "## 重要ドキュメント"
echo "- [完全版ロードマップ](${REPO_URL}/raw/${BRANCH}/docs/ROADMAP_COMPLETE.md)"
echo "- [プロジェクトマスター](${REPO_URL}/raw/${BRANCH}/docs/PROJECT_MASTER.md)"
echo "- [重要注意事項](${REPO_URL}/raw/${BRANCH}/docs/CRITICAL_NOTES.md)"

echo ""
echo "## 引き継ぎリソース"
echo "- [プロジェクト状態](${REPO_URL}/raw/${BRANCH}/PROJECT_STATUS.md)"
echo "- [引き継ぎ情報](${REPO_URL}/raw/${BRANCH}/PROJECT_HANDOVER.md)"
