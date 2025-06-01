#!/bin/bash
# HANAZONO マニュアルシステム起動スクリプト (修正版)

echo "🚀 HANAZONO マニュアルシステム起動 (修正版)..."

# 古いプロセスを停止
pkill -f "manual_auto_update.py"

# 権限設定
chmod +x manual_auto_update_fixed.py

# 初回更新
python3 manual_auto_update_fixed.py update

# 監視開始 (バックグラウンド)
nohup python3 manual_auto_update_fixed.py watch > manual_update.log 2>&1 &

echo "✅ マニュアルシステム起動完了"
echo "📖 マニュアル: HANAZONO_SYSTEM_MANUAL_v1.0.md"
echo "🔄 自動更新: 5分間隔"
echo "📋 ログ: manual_update.log"
echo "⏹️ 停止: pkill -f 'manual_auto_update_fixed.py'"
