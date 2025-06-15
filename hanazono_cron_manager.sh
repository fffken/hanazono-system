#!/bin/bash
# HANAZONOシステム cron管理
case "$1" in
    "status") crontab -l | grep -A 5 "HANAZONO" ;;
    "restore") crontab crontab_backup_20250615_211958.txt ;;
    "test") cd /home/pi/lvyuan_solar_control && python3 abc_integration_complete_test.py ;;
    *) echo "使用方法: bash $0 [status|restore|test]" ;;
esac