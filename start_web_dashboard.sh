#!/bin/bash
# HANAZONO Webダッシュボード常時稼働スクリプト

echo "🚀 HANAZONO Webダッシュボード起動..."

# 既存のWebサーバーを停止
pkill -f "web_dashboard_server.py"
pkill -f "flask"

# 権限設定
chmod +x web_dashboard_server.py

# バックグラウンドで起動
nohup python3 web_dashboard_server.py > web_dashboard.log 2>&1 &

sleep 2

echo "✅ Webダッシュボード起動完了"
echo "📊 アクセス URL: http://solarpi:8080"
echo "📊 ダッシュボード: http://solarpi:8080/dashboard"
echo "📖 マニュアル: http://solarpi:8080/manual"
echo "🔌 API: http://solarpi:8080/api/status"
echo "📋 ログ: web_dashboard.log"
echo "⏹️ 停止: pkill -f 'web_dashboard_server.py'"
