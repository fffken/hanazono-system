#!/bin/bash
# GitHub読み取り失敗時の代替引き継ぎ生成
cd ~/lvyuan_solar_control
echo "📋 ローカル引き継ぎ情報（GitHub読み取り失敗時用）" > LOCAL_HANDOVER.md
cat AI_WORK_RULES.md >> LOCAL_HANDOVER.md 2>/dev/null
cat PROJECT_STATUS.md >> LOCAL_HANDOVER.md 2>/dev/null
cat github_auto_handover.md >> LOCAL_HANDOVER.md 2>/dev/null
echo "✅ ローカル引き継ぎファイル生成完了: LOCAL_HANDOVER.md"
