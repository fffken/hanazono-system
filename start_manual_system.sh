#!/bin/bash
# HANAZONO マニュアルシステム起動スクリプト

echo "🚀 HANAZONO マニュアルシステム起動..."

chmod +x manual_auto_update.py

python3 manual_auto_update.py update

python3 manual_auto_update.py watch &

echo "✅ マニュアルシステム起動完了"
echo "📖 マニュアルファイル: HANAZONO_SYSTEM_MANUAL_v1.0.md"
echo "🔄 自動更新: 30秒間隔"
