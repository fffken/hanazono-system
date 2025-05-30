"""HANAZONOシステム自動最適化メインプログラム"""
import os
import re
import glob
import sys
import json
import logging
import time
import argparse
from datetime import datetime, timedelta
from lvyuan_collector import LVYUANCollector
from email_notifier import EmailNotifier
from settings_manager import SettingsManager
_hanazono_logger_instance = None

def collect_data():
    """
    インバーターからの現在のデータを収集し、保存します。

    Returns:
      bool: 収集・保存成功時はTrue、失敗時はFalse
    """
    logger = _hanazono_logger_instance
    try:
        settings_manager = SettingsManager()
        settings = settings_manager._settings
        collector = LVYUANCollector()
        data = collector.collect_data()
        if not data:
            logger.error('データ取得に失敗しました')
            return False
        os.makedirs('data', exist_ok=True)
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = f'data/lvyuan_data_{current_time}.json'
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
        logger.info(f'データを保存しました: {file_path}')
        return True
    except Exception as e:
        logger.error(f'データ収集エラー: {e}')
        import traceback
        logger.error(traceback.format_exc())
        return False

def send_daily_report():
    """
    日次レポートの送信処理を行います。

    前日データの有無に応じて、以下のフォールバック処理を実施します：
    1. 前日データがあれば、それを使用
    2. 前日データがなく当日データがあれば、当日データを使用
    3. 前日・当日データがなければ、利用可能な最新データを使用
    4. データが全く存在しなければ、管理者にアラートを送信

    Returns:
      bool: 送信成功時はTrue、失敗時はFalse
    """
    logger = _hanazono_logger_instance
    if logger is None:
        setup_logger()
        logger = _hanazono_logger_instance
    try:
        settings_manager = SettingsManager()
        settings = settings_manager._settings
        notifier = EmailNotifier(settings['email'], logger)
        settings = {}
        if not settings:
            logger.error('設定が正しく読み込まれていません')
            return False
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        yesterday_pattern = f'data/lvyuan_data_{yesterday}_*.json'
        yesterday_files = glob.glob(yesterday_pattern)
        today = datetime.now().strftime('%Y%m%d')
        today_pattern = f'data/lvyuan_data_{today}_*.json'
        today_files = glob.glob(today_pattern)
        all_files = glob.glob('data/lvyuan_data_*.json')
        target_files = yesterday_files or today_files or sorted(all_files, reverse=True)[:1]
        if not target_files:
            logger.warning('データファイルが見つかりません')
            return False
        latest_file = sorted(target_files, reverse=True)[0]
        logger.info(f'レポート生成に使用するファイル: {latest_file}')
        try:
            with open(latest_file, 'r') as data_file:
                solar_data = json.load(data_file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f'データファイル読み込みエラー: {e}')
            return False
        weather_info = {}
        try:
            weather_file = 'data/weather_data.json'
            if os.path.exists(weather_file):
                with open(weather_file, 'r') as w_file:
                    weather_info = json.load(w_file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f'天気データ読み込みエラー: {e}')
        report_data = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'source_file': latest_file, 'solar_data': solar_data, 'weather': weather_info}
        success = notifier.send_daily_report(report_data)
        if success:
            logger.info('日次レポート送信成功')
        else:
            logger.error('日次レポート送信失敗')
        return success
    except Exception as e:
        logger.error(f'実行エラー: {e}')
        import traceback
        logger.error(traceback.format_exc())
        return False

def check_cron_job():
    """
    cronジョブが正しく設定されているか確認します。

    Returns:
      bool: 確認成功時はTrue、失敗時はFalse
    """
    logger = _hanazono_logger_instance
    try:
        import subprocess
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error('cronジョブの確認に失敗しました')
            return False
        cron_content = result.stdout
        collect_job_pattern = re.compile('.*python.*--collect.*')
        report_job_pattern = re.compile('.*python.*--daily-report.*')
        has_collect_job = any((collect_job_pattern.match(line) for line in cron_content.split('\n')))
        has_report_job = any((report_job_pattern.match(line) for line in cron_content.split('\n')))
        if not has_collect_job:
            logger.warning('データ収集用のcronジョブが設定されていません')
        if not has_report_job:
            logger.warning('レポート送信用のcronジョブが設定されていません')
        if has_collect_job and has_report_job:
            logger.info('cronジョブは正しく設定されています')
            return True
        else:
            return False
    except Exception as e:
        logger.error(f'cronジョブ確認エラー: {e}')
        return False

def setup_logger():
    """
    ロギングの設定を行い、ロガーインスタンスを返します。

    Returns:
        logging.Logger: 設定済みのロガーインスタンス
    """
    global _hanazono_logger_instance
    if _hanazono_logger_instance:
        return _hanazono_logger_instance
    os.makedirs('logs', exist_ok=True)
    logger = logging.getLogger('hanazono_logger')
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    file_handler = logging.FileHandler('logs/hanazono.log')
    file_handler.setLevel(logging.INFO)
    error_handler = logging.FileHandler('logs/hanazono_error.log')
    error_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    _hanazono_logger_instance = logger
    return logger

def main():
    """
    メイン処理フロー
    """
    global _hanazono_logger_instance
    _hanazono_logger_instance = setup_logger()
    logger = _hanazono_logger_instance
    logger.info('HANAZONOシステム自動最適化を開始します')
    parser = argparse.ArgumentParser(description='HANAZONO自動最適化システム')
    parser.add_argument('--collect', action='store_true', help='現在のデータを収集し保存します')
    parser.add_argument('--daily-report', action='store_true', help='日次レポートを生成して送信します')
    parser.add_argument('--check-cron', action='store_true', help='cronジョブの設定を確認します')
    parser.add_argument('--debug', action='store_true', help='デバッグモードで実行します')
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)
        logger.debug('デバッグモードで実行中')
    try:
        if args.collect:
            collect_data()
        if args.daily_report:
            logger.info('日次レポート送信を開始します')
            send_daily_report()
        if args.check_cron:
            check_cron_job()
        if not (args.collect or args.daily_report or args.check_cron):
            logger.info('動作モードが指定されていません。--help でヘルプを表示します')
            print('使用方法: python3 main.py [オプション]')
            print('オプション:')
            print('  --collect       データ収集を実行')
            print('  --daily-report  日次レポートを送信')
            print('  --check-cron    cronジョブの設定を確認')
            print('  --debug         デバッグモードで実行')
    except Exception as e:
        logger.error(f'実行エラー: {e}')
        import traceback
        logger.error(traceback.format_exc())
    logger.info('HANAZONOシステム自動最適化を終了します')
if __name__ == '__main__':
    main()