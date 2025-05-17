#!/bin/bash
# HANAZONOシステム GitHub効率連携スクリプト v2.0

echo "=== HANAZONOシステム GitHub効率連携 $(date) ==="

# 基本情報収集
echo "## 基本リポジトリ情報"
git remote -v
git branch -v

# 変更状態確認
echo "## 最新の変更を確認"
git status

# コアファイル情報
echo "## コアファイル情報"
for file in main.py email_notifier.py settings_manager.py; do
  if [ -f "$file" ]; then
    echo "$file: 最終更新 $(date -r "$file" +%Y-%m-%d), $(wc -l < "$file") 行"
    # 主要関数一覧も追加
    echo "  主要関数:"
    grep -n "def " "$file" | head -5 | sed 's/^/    /'
  fi
done

# README情報
echo "## README概要"
if [ -f "README.md" ]; then
  head -10 README.md
fi

# プロジェクト状態
echo "## プロジェクト状態"
if [ -f "PROJECT_STATUS.md" ]; then
  cat PROJECT_STATUS.md | head -20
fi
if [ -f "PROJECT_HANDOVER.md" ]; then
  echo "## 引き継ぎ情報 (PROJECT_HANDOVER.md)"
  echo "引き継ぎ情報ファイルが存在します。新しいセッションでこのファイルを共有してください。"
fi

# 最近のコミット履歴
echo "## プロジェクト履歴"
git log --oneline -n 5

echo ""
echo ""
echo "このスクリプトの出力結果をコピーして、AIに共有することで効率的な支援を受けられます"
