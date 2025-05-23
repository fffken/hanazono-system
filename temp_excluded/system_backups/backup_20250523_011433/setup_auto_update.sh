#!/bin/bash
# 自動更新システムのCron設定

echo "=== HANAZONOシステム 自動更新設定 ==="

# 現在のcrontabをバックアップ
crontab -l > cron_backup_$(date +%Y%m%d).txt 2>/dev/null
echo "✅ 現在のcrontabをバックアップしました"

# 新しいcrontab設定
(
crontab -l 2>/dev/null | grep -v "HANAZONOシステム" | grep -v "master_progress_controller"
echo "# HANAZONOシステム 自動進行管理"
echo "*/30 * * * * cd /home/pi/lvyuan_solar_control && bash scripts/master_progress_controller.sh update-only"
echo "0 0 * * * cd /home/pi/lvyuan_solar_control && bash scripts/master_progress_controller.sh full"
) | crontab -

echo "✅ 自動更新システムをCronに登録しました"
echo "- 30分ごと: 状態更新"
echo "- 毎日0時: 完全更新"

# 設定確認
echo ""
echo "=== 設定されたCronジョブ ==="
crontab -l | grep -E "(HANAZONOシステム|master_progress_controller)"

