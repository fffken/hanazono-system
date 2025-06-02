#!/bin/bash
# 真の自動入力システム

TASK_NAME="$1"
DESCRIPTION="$2"

# 一時的な入力ファイル作成
cat > /tmp/auto_input.txt << INPUT_EOF
1
$TASK_NAME
$DESCRIPTION
INPUT_EOF

# 自動入力実行
bash scripts/enhanced_auto_file_generator.sh < /tmp/auto_input.txt
rm /tmp/auto_input.txt
