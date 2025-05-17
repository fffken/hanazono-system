#!/bin/bash
# 引き継ぎ情報一括生成スクリプト（更新版）

echo "=== HANAZONOシステム 引き継ぎ情報生成 $(date) ==="
echo "引き継ぎ情報をファイルに保存します..."

# 引き継ぎプロンプト
echo "# HANAZONOシステム 引き継ぎパック" > handover_pack.md
echo "作成日時: $(date)" >> handover_pack.md
echo "" >> handover_pack.md

# 基本情報
echo "## 1. 基本引き継ぎ情報" >> handover_pack.md
cat PROJECT_HANDOVER.md >> handover_pack.md
echo "" >> handover_pack.md

# GitHub状態
echo "## 2. GitHub状態情報" >> handover_pack.md
bash scripts/github_efficiency.sh >> handover_pack.md 2>/dev/null
echo "" >> handover_pack.md

# 重要情報
echo "## 3. 重要プロジェクト情報" >> handover_pack.md
echo "以下の情報を取得するには:" >> handover_pack.md
echo '```bash' >> handover_pack.md
echo "bash scripts/get_essential_info.sh" >> handover_pack.md
echo '```' >> handover_pack.md
echo "" >> handover_pack.md

# Raw URL生成
echo "## 4. ファイル直接リンク" >> handover_pack.md
bash scripts/generate_raw_links.sh >> handover_pack.md 2>/dev/null

echo "引き継ぎ情報パックを handover_pack.md に保存しました"
echo "次のAIセッションでは、このファイルの内容をコピーして共有してください"
