#!/bin/bash
# cron構文自動修正システム v2.0 - 完全版

echo "🔧 cron構文自動修正 v2.0 開始"

# バックアップ
BACKUP_FILE="/tmp/crontab_backup_$(date +%Y%m%d_%H%M%S)"
crontab -l > "$BACKUP_FILE" 2>/dev/null || echo "" > "$BACKUP_FILE"
echo "📁 バックアップ: $BACKUP_FILE"

# 完全修正版生成
FIXED_FILE="/tmp/crontab_fixed_$(date +%Y%m%d_%H%M%S)"

cat << 'EOF' > "$FIXED_FILE"
*/15 * * * * /bin/bash -c "cd /home/pi/lvyuan_solar_control && source venv/bin/activate && python3 main.py --collect" > /dev/null 2>&1
0 7 * * * /bin/bash -c "cd /home/pi/lvyuan_solar_control && source venv/bin/activate && python3 main.py --daily-report" >> /home/pi/lvyuan_solar_control/logs/cron_daily_report_morning.log 2>&1
0 23 * * * /bin/bash -c "cd /home/pi/lvyuan_solar_control && source venv/bin/activate && python3 main.py --daily-report" >> /home/pi/lvyuan_solar_control/logs/cron_daily_report_night.log 2>&1
0 0 * * * cd /home/pi/lvyuan_solar_control && bash scripts/auto_update/update_handover.sh
0 7,19 * * * cd /home/pi/lvyuan_solar_control && python3 -c 'from system_health_monitor import run_controlled_health_check; run_controlled_health_check()' >> logs/daily_health.log 2>&1
0 3 * * * cd /home/pi/lvyuan_solar_control && python3 hanazono_optimizer.py standard >> logs/auto_optimize.log 2>&1
0 6 * * * cd /home/pi/lvyuan_solar_control && python3 hanazono_optimizer.py health >> logs/auto_health.log 2>&1
5 0 * * * cd /home/pi/lvyuan_solar_control && bash scripts/backup_handover_generator.sh >> logs/backup_handover.log 2>&1
0 */2 * * * python3 self_evolving_ai_v3.py --auto-evolve
*/15 * * * * python3 self_evolving_ai_v3.py --health-check
0 * * * * cd /home/pi/lvyuan_solar_control && bash scripts/auto_git_save_system.sh >> logs/auto_git_save.log 2>&1
EOF

# 適用
crontab "$FIXED_FILE"
echo "✅ cron完全修正完了"

# 確認
echo "📋 修正結果確認:"
crontab -l | grep -E "(auto_git_save|collect|daily-report)"
EOF
