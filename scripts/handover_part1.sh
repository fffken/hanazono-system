#!/bin/bash
# HANAZONOシステム 引き継ぎプロンプト生成 パート1：基本情報

# 色の設定
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# 現在の日付
CURRENT_DATE=$(date +%Y%m%d)
VERSION=1

# 以前の引き継ぎプロンプトからバージョン番号を取得
if [ -f "HANDOVER_PROMPT.md" ]; then
  prev_version=$(grep -o "v[0-9]\+" HANDOVER_PROMPT.md | head -n 1 | tr -d 'v')
  if [ ! -z "$prev_version" ]; then
    VERSION=$((prev_version + 1))
  fi
fi

# プロンプトのヘッダー部分
cat > HANDOVER_PROMPT_PART1.md << EOF
# v${VERSION}_HANAZONOシステム／詳細引き継ぎプロンプト-${CURRENT_DATE}

## プロジェクト全体概要
HANAZONOシステムは、Raspberry Pi Zero 2 W上で動作するソーラー蓄電システム(LVYUAN SPI-10K-U)の自動最適化ソリューションです。GitHub(https://github.com/fffken/hanazono-system)で管理されている Python プロジェクトで、15分ごとのデータ収集と1日2回（7時・23時）のレポートメール送信機能を提供します。現在は$(grep -A 1 "現在のフェーズ" PROJECT_STATUS.md 2>/dev/null | tail -n 1 | cut -d':' -f2- | sed 's/^[ \t]*//;s/[ \t]*$//' || echo "開発プロセス改善・安定化フェーズ")に注力しています。
EOF

echo -e "${GREEN}パート1の引き継ぎプロンプトを生成しました${NC}"
