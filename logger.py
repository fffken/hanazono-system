#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
import datetime
from config import LOG_FILE

# ログ設定


def setup_logger():
    """ロガーをセットアップ"""
    logger = logging.getLogger("solar_control")
    logger.setLevel(logging.INFO)

    # ファイルハンドラ（ローテーション機能付き）
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # コンソールへの出力も設定
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(file_format)
    logger.addHandler(console_handler)

    return logger


# グローバルロガーインスタンス
logger = setup_logger()


def log_settings(weather_data, season, settings_type, settings):
    """
    設定情報をログに記録

    引数:
        weather_data: 天気予報データ
        season: 季節 ('winter', 'spring_fall', 'summer')
        settings_type: 設定タイプ ('typeA' or 'typeB')
        settings: 適用する設定値
    """
    season_names = {
        'winter': '冬季',
        'spring_fall': '春秋季',
        'summer': '夏季'
    }

    type_names = {
        'typeA': 'タイプA（控えめ設定）',
        'typeB': 'タイプB（標準設定）'
    }

    logger.info("----- 設定推奨 -----")
    logger.info(
        f"天気: 今日={weather_data['today']['weather']}, 明日={weather_data['tomorrow']['weather']}")
    logger.info(f"季節: {season_names.get(season, season)}")
    logger.info(f"推奨設定: {type_names.get(settings_type, settings_type)}")
    logger.info(f"充電電流: {settings['charge_current']}A (ID: 07)")
    logger.info(f"充電時間: {settings['charge_time']}分 (ID: 10)")
    logger.info(f"SOC設定: {settings['soc']}% (ID: 62)")
    logger.info("-------------------")
