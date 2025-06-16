#!/bin/bash
# HANAZONOシステム 運用最適化管理スクリプト
# 作成日時: 2025年06月15日 22:40:35

echo "⚡ HANAZONOシステム 運用最適化管理"
echo "=" * 60

case "$1" in
    "status")
        echo "📊 システム状況確認:"
        crontab -l | grep -A 15 -B 2 "HANAZONO"
        echo ""
        echo "📈 最近のログ状況:"
        ls -la /tmp/hanazono_*.log 2>/dev/null | tail -5 || echo "ログなし"
        ;;
    "logs")
        echo "📋 詳細ログ確認:"
        echo "🌅 朝のログ（最新5行）:"
        tail -5 /tmp/hanazono_morning.log 2>/dev/null || echo "ログなし"
        echo "🌙 夜のログ（最新5行）:"  
        tail -5 /tmp/hanazono_evening.log 2>/dev/null || echo "ログなし"
        echo "📊 週次ログ（最新5行）:"
        tail -5 /tmp/hanazono_weekly.log 2>/dev/null || echo "ログなし"
        echo "🔧 月次ログ（最新5行）:"
        tail -5 /tmp/hanazono_monthly.log 2>/dev/null || echo "ログなし"
        ;;
    "monitor")
        echo "🔍 リアルタイム監視:"
        python3 -c "
import glob
import datetime
import os
print('📊 システム監視レポート', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
logs = glob.glob('/tmp/hanazono_*.log')
print(f'📁 ログファイル: {len(logs)}個')
for log in logs:
    try:
        mtime = os.path.getmtime(log)
        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%m-%d %H:%M')
        size = os.path.getsize(log)
        print(f'📄 {os.path.basename(log)}: {mtime_str} ({size}B)')
    except:
        print(f'❌ {log}: 読み取りエラー')
"
        ;;
    "test")
        echo "🧪 手動テスト実行:"
        cd /home/pi/lvyuan_solar_control
        python3 abc_integration_icon_fixed_20250615_223350.py
        ;;
    "clean")
        echo "🗑️ ログクリーンアップ:"
        rm -f /tmp/hanazono_*.log
        echo "✅ ログファイル削除完了"
        ;;
    "restore")
        echo "🔄 元のcron設定に復旧..."
        if [ -f "crontab_optimization_backup_20250615_224035.txt" ]; then
            crontab crontab_optimization_backup_20250615_224035.txt
            echo "✅ 復旧完了"
        else
            echo "❌ バックアップファイル未発見"
        fi
        ;;
    "performance")
        echo "📈 パフォーマンス確認:"
        echo "💾 ディスク使用量:"
        df -h /home/pi/lvyuan_solar_control | tail -1
        echo "🔄 メモリ使用量:"
        free -h | grep Mem
        echo "⚡ システム負荷:"
        uptime
        ;;
    *)
        echo "🔧 HANAZONOシステム 運用最適化管理コマンド:"
        echo "  bash $0 status      # システム状況確認"
        echo "  bash $0 logs        # 詳細ログ確認"
        echo "  bash $0 monitor     # リアルタイム監視"
        echo "  bash $0 test        # 手動テスト実行"
        echo "  bash $0 clean       # ログクリーンアップ"
        echo "  bash $0 performance # パフォーマンス確認"
        echo "  bash $0 restore     # 元設定に復旧"
        ;;
esac
