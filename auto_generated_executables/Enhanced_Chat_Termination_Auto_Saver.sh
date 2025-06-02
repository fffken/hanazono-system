#!/bin/bash

# === 強化版チャット容量制限自動保存システム ===
echo "🚨 強化版チャット容量制限自動保存システム開始..."

# ファイル設定
AUTO_SAVE_FILE="CHAT_TERMINATION_AUTO_SAVE.md"
EMERGENCY_PROMPT="EMERGENCY_HANDOVER_PROMPT.md"
TIMESTAMP=$(date)

# 現在の進行状況を動的取得
current_task=$(ls auto_generated_executables/*.sh | tail -1 | xargs basename)
git_changes=$(git status --porcelain | wc -l)
last_commit=$(git log -1 --oneline)

echo "📊 現在状況取得完了"
echo "現在タスク: $current_task"
echo "Git変更: $git_changes 件"


# 強化版緊急プロンプト生成
cat > $EMERGENCY_PROMPT << ENHANCED_PROMPT
# 🚨 強化版緊急引き継ぎプロンプト

*緊急保存時刻*: $TIMESTAMP
*継承レベル*: 100%完全記憶継承 + 即座作業再開

## ⚡ 即座作業再開手順（3分で完全復帰）

### STEP 1: 環境確認・復帰
\`\`\`bash
cd ~/lvyuan_solar_control
pwd
\`\`\`

### STEP 2: 現在状況の完全把握
\`\`\`bash
bash scripts/master_progress_controller.sh
cat CHAT_TERMINATION_AUTO_SAVE.md | head -20
\`\`\`

### STEP 3: 具体的次回アクション
*現在の進行*: $current_task 関連作業
*Git状態*: $git_changes 件未コミット
*最新コミット*: $last_commit

*次に実行すべきコマンド*:
\`\`\`bash
echo "現在の作業: $current_task"
ls auto_generated_executables/ | tail -5
\`\`\`

## 🎯 期待される結果
- 3分以内での完全状況把握
- 具体的な次のアクション明確化
- 中断感ゼロでの作業継続

ENHANCED_PROMPT

echo "✅ 強化版緊急引き継ぎプロンプト生成完了"
echo "🎯 即座作業再開機能実装完了"

