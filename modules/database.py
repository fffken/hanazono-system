"""SQLiteデータベース管理モジュール"""
import os
import re
import json
import glob
import sqlite3
import logging
from datetime import datetime
logger = logging.getLogger('database')

class DatabaseManager:
    """LVYUANソーラーシステムのデータベース管理クラス"""

    def __init__(self, db_file=None, settings_file=None):
        """
        データベース管理クラスの初期化

        Args:
            db_file: データベースファイルのパス（指定がなければ設定から読み込み）
            settings_file: 設定ファイルのパス
        """
        if settings_file is None:
            self.settings_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'settings.json')
        else:
            self.settings_file = settings_file
        self.settings = self._load_settings()
        if db_file is None:
            db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), self.settings.get('files', {}).get('data_directory', 'data'), 'db')
            os.makedirs(db_dir, exist_ok=True)
            self.db_file = os.path.join(db_dir, 'lvyuan_solar.db')
        else:
            self.db_file = db_file
        logger.info(f'データベースファイル: {self.db_file}')

    def _load_settings(self):
        """設定ファイルの読み込み"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            else:
                logger.error(f'設定ファイルが見つかりません: {self.settings_file}')
                return {}
        except Exception as e:
            logger.error(f'設定ファイル読み込みエラー: {e}')
            return {}

    def init_db(self):
        """
        データベースの初期化とテーブル作成

        Returns:
            bool: 成功時はTrue、失敗時はFalse
        """
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('\n            CREATE TABLE IF NOT EXISTS measurements (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                timestamp TEXT NOT NULL,\n                date TEXT NOT NULL,\n                time TEXT NOT NULL,\n                parameter_id TEXT NOT NULL,\n                parameter_name TEXT NOT NULL,\n                value REAL NOT NULL,\n                unit TEXT,\n                UNIQUE(timestamp, parameter_id)\n            )\n            ')
            cursor.execute('\n            CREATE TABLE IF NOT EXISTS daily_summary (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                date TEXT UNIQUE NOT NULL,\n                battery_soc_min REAL,\n                battery_soc_max REAL,\n                battery_soc_avg REAL,\n                grid_import_total REAL,\n                grid_export_total REAL,\n                pv_production_total REAL,\n                battery_charge_total REAL,\n                battery_discharge_total REAL,\n                load_total REAL,\n                weather_summary TEXT,\n                notes TEXT\n            )\n            ')
            cursor.execute('\n            CREATE TABLE IF NOT EXISTS weather_data (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                timestamp TEXT NOT NULL,\n                date TEXT NOT NULL,\n                time TEXT NOT NULL,\n                temperature REAL,\n                humidity REAL,\n                weather_condition TEXT,\n                forecast TEXT,\n                UNIQUE(timestamp)\n            )\n            ')
            cursor.execute('\n            CREATE TABLE IF NOT EXISTS parameter_settings (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                timestamp TEXT NOT NULL,\n                parameter_id TEXT NOT NULL,\n                parameter_name TEXT NOT NULL,\n                value REAL NOT NULL,\n                previous_value REAL,\n                change_reason TEXT,\n                notes TEXT,\n                UNIQUE(timestamp, parameter_id)\n            )\n            ')
            conn.commit()
            conn.close()
            logger.info('データベース初期化成功')
            return True
        except Exception as e:
            logger.error(f'データベース初期化エラー: {e}')
            return False

    def import_json_data(self, json_file):
        """
        JSONデータをデータベースにインポートする

        Args:
            json_file: インポートするJSONファイルのパス

        Returns:
            bool: 成功時はTrue、失敗時はFalse
        """
        try:
            with open(json_file, 'r') as f:
                data_list = json.load(f)
            if not isinstance(data_list, list):
                data_list = [data_list]
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            total_inserted = 0
            for data in data_list:
                if 'timestamp' in data:
                    timestamp = data.get('datetime', str(datetime.fromtimestamp(data['timestamp'])))
                else:
                    filename = os.path.basename(json_file)
                    match = re.search('_(\\d{8})\\.json$', filename)
                    date_str = match.group(1) if match else datetime.now().strftime('%Y%m%d')
                    timestamp = f'{date_str}T12:00:00'
                try:
                    dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                    date = dt.strftime('%Y-%m-%d')
                    time = dt.strftime('%H:%M:%S')
                except ValueError:
                    dt = datetime.fromtimestamp(data['timestamp'])
                    date = dt.strftime('%Y-%m-%d')
                    time = dt.strftime('%H:%M:%S')
                if 'parameters' in data:
                    parameters = data['parameters']
                    for param_id, param_info in parameters.items():
                        param_name = param_info.get('name', '')
                        value = param_info.get('value', 0)
                        unit = param_info.get('unit', '')
                        cursor.execute('\n                        INSERT OR REPLACE INTO measurements\n                        (timestamp, date, time, parameter_id, parameter_name, value, unit)\n                        VALUES (?, ?, ?, ?, ?, ?, ?)\n                        ', (timestamp, date, time, param_id, param_name, value, unit))
                        total_inserted += 1
            conn.commit()
            conn.close()
            logger.info(f'JSONデータのインポート成功: {json_file} ({total_inserted} レコード)')
            return True
        except Exception as e:
            logger.error(f'JSONデータのインポートエラー: {e}')
            import traceback
            logger.debug(traceback.format_exc())
            return False

    def import_all_json_data(self, json_dir=None, file_pattern='data_*.json'):
        """
        指定ディレクトリにある全てのJSONファイルをインポートする

        Args:
            json_dir: JSONファイルのディレクトリ（指定がなければ標準データディレクトリ）
            file_pattern: インポートするファイルのパターン

        Returns:
            tuple: (成功件数, 失敗件数)
        """
        try:
            if json_dir is None:
                json_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), self.settings.get('files', {}).get('data_directory', 'data'))
            json_files = glob.glob(os.path.join(json_dir, file_pattern))
            if not json_files:
                logger.warning(f'インポートするJSONファイルが見つかりません: {os.path.join(json_dir, file_pattern)}')
                return (0, 0)
            success_count = 0
            failed_count = 0
            for file in json_files:
                if self.import_json_data(file):
                    success_count += 1
                else:
                    failed_count += 1
            logger.info(f'JSONデータのインポート完了: 成功 {success_count} 件, 失敗 {failed_count} 件')
            return (success_count, failed_count)
        except Exception as e:
            logger.error(f'JSONデータの一括インポートエラー: {e}')
            return (0, 0)
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='LVYUANソーラーデータベース管理ツール')
    parser.add_argument('--init', action='store_true', help='データベースを初期化する')
    parser.add_argument('--import', dest='import_file', help='指定したJSONファイルをインポートする')
    parser.add_argument('--import-all', action='store_true', help='全てのJSONファイルをインポートする')
    parser.add_argument('--pattern', default='data_*.json', help='インポートするJSONファイルのパターン（デフォルト: data_*.json）')
    parser.add_argument('--verbose', '-v', action='store_true', help='詳細なログを出力する')
    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)
    db_manager = DatabaseManager()
    if args.init:
        db_manager.init_db()
    if args.import_file:
        db_manager.import_json_data(args.import_file)
    if args.import_all:
        db_manager.import_all_json_data(file_pattern=args.pattern)
    if not (args.init or args.import_file or args.import_all):
        db_manager.init_db()