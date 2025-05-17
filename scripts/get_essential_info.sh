#!/bin/bash
# 重要プロジェクト情報抽出スクリプト

echo "# HANAZONOシステム 必須プロジェクト情報"
echo ""

echo "## 1. プロジェクトマスター情報 (PROJECT_MASTER.md)"
echo ""
if [ -f "docs/PROJECT_MASTER.md" ]; then
  cat "docs/PROJECT_MASTER.md"
else
  echo "PROJECT_MASTER.md が見つかりません"
fi

echo ""
echo "## 2. プロジェクトロードマップ情報 (roadmap.md)"
echo ""
if [ -f "docs/project/roadmap.md" ]; then
  cat "docs/project/roadmap.md"
else
  echo "roadmap.md が見つかりません"
fi

echo ""
echo "## 3. 重要な注意事項 (CRITICAL_NOTES.md)"
echo ""
if [ -f "docs/CRITICAL_NOTES.md" ]; then
  cat "docs/CRITICAL_NOTES.md"
else
  echo "CRITICAL_NOTES.md が見つかりません"
fi

echo ""
echo "## 4. ローカルPDFファイル情報"
echo ""
echo "以下のPDFファイルがローカルに存在します（GitHubには追加されていません）:"
find docs -name "*.pdf" | sort
