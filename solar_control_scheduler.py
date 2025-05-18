#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import subprocess
import datetime
import os
from logger import logger

# メインプログラムのパス
MAIN_PROGRAM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")

def run_solar_control():
    """
    solar_controlプログラムを実行
    """
    try:
        # Pythonスクリプトを実行
        logger.info("メインプログラムを実行します...")
        process = subprocess.run(["python3", MAIN_PROGRAM], capture_output=True, text=True)
        
        # 出力をログに記録
        if process.stdout:
            for line in process.stdout.splitlines():
                logger.info(f"出力: {line}")
                
        # エラーをログに記録
        if process.returncode != 0:
            logger.error(f"メインプログラムがエラーで終了しました。リターンコード: {process.returncode}")
            if process.stderr:
                for line in process.stderr.splitlines():
                    logger.error(f"エラー出力: {line}")
        else:
            logger.info("メインプログラムが正常終了しました")
            
    except Exception as e:
        logger.error(f"スケジューラでエラーが発生しました: {str(e)}")

def run_scheduled():
    """
    スケジュールに従ってプログラム実行
    """
    while True:
        # 現在の時間を取得
        now = datetime.datetime.now()
        logger.info(f"スケジューラ: 現在時刻 {now.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 朝6時と夕方16時に実行
        if now.hour in [6, 16] and now.minute == 0:
            logger.info("スケジュール時間に達しました。プログラムを実行します...")
            run_solar_control()
        
        # 1分間隔でチェック
        time.sleep(60)

if __name__ == "__main__":
    logger.info("========= ソーラー制御スケジューラを開始します =========")
    try:
        # 起動時に一度実行
        run_solar_control()
        
        # スケジュール実行を開始
        run_scheduled()
    except KeyboardInterrupt:
        logger.info("スケジューラを終了します（Ctrl+Cが押されました）")
    except Exception as e:
        logger.error(f"スケジューラ実行中にエラーが発生しました: {str(e)}")
