#!/bin/bash

# スクリプトがある場所をカレントディレクトリに設定
cd "$(dirname "$0")"

# 既存プロセスの確認と終了
PID=$(pgrep -f "python3 solar_control_scheduler.py")
if [ ! -z "$PID" ]; then
    echo "既存のスケジューラプロセス(PID: $PID)を終了します..."
    kill $PID
    sleep 2
fi

# スケジューラを起動
echo "ソーラー制御スケジューラを起動します..."
nohup python3 solar_control_scheduler.py > scheduler.log 2>&1 &

# 起動確認
sleep 2
NEW_PID=$(pgrep -f "python3 solar_control_scheduler.py")
if [ ! -z "$NEW_PID" ]; then
    echo "スケジューラが起動しました(PID: $NEW_PID)"
else
    echo "スケジューラの起動に失敗しました"
fi
