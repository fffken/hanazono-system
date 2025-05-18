#!/bin/bash
# パート1: 基本情報

CURRENT_DATE=$(date +%Y%m%d)
VERSION=1

# バージョン番号の取得
if [ -f "HANDOVER_PROMPT.md" ]; then
  prev_version=$(grep -o "v[0-9]\+" HANDOVER_PROMPT.md | head -n 1 | tr -d 'v')
  if [ ! -z "$prev_version" ]; then
    VERSION=$((prev_version + 1))
  fi
fi

cat > docs/handover_part1.md << EOF
# v${VERSION}_HANAZONOシステム／詳細引き継ぎプロンプト-${CURRENT_DATE}

## プロジェクト全体概要
HANAZONOシステムは、Raspberry Pi Zero 2 W上で動作するソーラー蓄電システム(LVYUAN SPI-10K-U)の自動最適化ソリューションです。GitHub(https://github.com/fffken/hanazono-system)で管理されている Python プロジェクトで、15分ごとのデータ収集と1日2回（7時・23時）のレポートメール送信機能を提供します。現在は開発プロセス改善・安定化フェーズに注力しています。
EOF

echo "パート1作成完了"
