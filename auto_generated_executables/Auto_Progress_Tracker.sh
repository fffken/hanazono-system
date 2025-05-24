#!/bin/bash

# === 進行状況自動追跡システム ===
echo "📊 進行状況自動追跡システム実行中..."

# 自動検出・更新
bash scripts/update_progress_tracker.sh

# master_progress_controllerに統合
echo "🔗 master_progress_controllerに自動統合中..."
if ! grep -q "Auto_Progress_Tracker" scripts/master_progress_controller.sh; then
    sed -i '/完全自動進行管理システム実行完了/i bash auto_generated_executables/Auto_Progress_Tracker.sh' scripts/master_progress_controller.sh
    echo "✅ 自動統合完了"
else
    echo "✅ 既に統合済み"
fi

echo "🎯 今後は完全自動実行されます"
