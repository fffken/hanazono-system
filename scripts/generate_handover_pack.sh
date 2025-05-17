#!/bin/bash
# 引き継ぎ情報一括生成スクリプト

echo "=== HANAZONOシステム 引き継ぎ情報生成 $(date) ==="
echo "引き継ぎ情報をファイルに保存します..."

# 引き継ぎプロンプト
echo "## 1. 基本引き継ぎ情報"
cat PROJECT_HANDOVER.md > handover_pack.md
echo "" >> handover_pack.md

# GitHub状態
echo "## 2. GitHub状態情報" >> handover_pack.md
bash scripts/github_efficiency.sh >> handover_pack.md
echo "" >> handover_pack.md

# Raw URL生成
echo "## 3. ファイル直接リンク" >> handover_pack.md
bash scripts/generate_raw_links.sh >> handover_pack.md

echo "引き継ぎ情報パックを handover_pack.md に保存しました"
echo "次のAIセッションでは、このファイルの内容をコピーして共有してください"
