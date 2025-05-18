#!/bin/bash
# HANAZONOシステム バックアップ・変更管理スクリプト

# 使用方法: ./backup_and_change.sh <filename> <change_id> <brief_description>
# 例: ./backup_and_change.sh email_notifier.py HANA-EMAIL-001 "メール形式を修正"

if [ $# -lt 3 ]; then
  echo "使用方法: $0 <filename> <change_id> <brief_description>"
  exit 1
fi

FILENAME=$1
CHANGE_ID=$2
DESCRIPTION=$3
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP="${FILENAME}.bak_${DATE}"

# バックアップ作成
cp "$FILENAME" "$BACKUP"
echo "バックアップ作成完了: $BACKUP"

# 変更ログエントリ作成
cat >> CHANGELOG.md << EOF

## ${CHANGE_ID}: ${DESCRIPTION}
日時: $(date "+%Y-%m-%d %H:%M:%S")
バックアップ: ${BACKUP}
EOF

# エディタでファイルを開く
if [ -n "$EDITOR" ]; then
  $EDITOR "$FILENAME"
else
  nano "$FILENAME"
fi

echo "変更が完了したら、以下のコマンドでテストとコミットを行ってください:"
echo "python3 main.py --daily-report --debug  # テスト実行"
echo "git add $FILENAME CHANGELOG.md"
echo "git commit -m \"${CHANGE_ID}: ${DESCRIPTION}\""
