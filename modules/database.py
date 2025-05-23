#!/usr/bin/env python3
"""SQLiteデータベース管理モジュール"""

import os
import re
import json
import glob
import sqlite3
import logging
from datetime import datetime

# ロガー設定
logger = logging.getLogger("database")


class DatabaseManager:
    """LVYUANソーラーシステムのデータベース管理クラス"""

    def __init__(self, db_file=None, settings_file=None):
        """
        データベース管理クラスの初期化

        Args:
            db_file: データベースファイルのパス（指定がなければ設定から読み込み）
            settings_file: 設定ファイルのパス
        """
        # 設定ファイルのパス
        if settings_file is None:
            self.settings_file = os.path.join(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))), 'settings.json')
        else:
            self.settings_file = settings_file

        # 設定の読み込み
        self.settings = self._load_settings()

        # データベースファイルのパス
        if db_file is None:
            db_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                self.settings.get('files', {}).get('data_directory', 'data'),
                'db'
            )
            os.makedirs(db_dir, exist_ok=True)
            self.db_file = os.path.join(db_dir, 'lvyuan_solar.db')
        else:
            self.db_file = db_file

        logger.info(f"データベースファイル: {self.db_file}")

    def _load_settings(self):
        """設定ファイルの読み込み"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            else:
                logger.error(f"設定ファイルが見つかりません: {self.settings_file}")
                return {}
        except Exception as e:
            logger.error(f"設定ファイル読み込みエラー: {e}")
            return {}

    def init_db(self):
        """
        データベースの初期化とテーブル作成

        Returns:
            bool: 成功時はTrue、失敗時はFalse
        """
        try:
            # データベース接続
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # テーブル作成：measurements（測定データ）
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                parameter_id TEXT NOT NULL,
                parameter_name TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT,
                UNIQUE(timestamp, parameter_id)
            )
            ''')

            # テーブル作成：daily_summary（日次サマリー）
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,
                battery_soc_min REAL,
                battery_soc_max REAL,
                battery_soc_avg REAL,
                grid_import_total REAL,
                grid_export_total REAL,
                pv_production_total REAL,
                battery_charge_total REAL,
                battery_discharge_total REAL,
                load_total REAL,
                weather_summary TEXT,
                notes TEXT
            )
            ''')

            # テーブル作成：weather_data（気象データ）
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                temperature REAL,
                humidity REAL,
                weather_condition TEXT,
                forecast TEXT,
                UNIQUE(timestamp)
            )
            ''')

            # テーブル作成：parameter_settings（パラメータ設定履歴）
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS parameter_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                parameter_id TEXT NOT NULL,
                parameter_name TEXT NOT NULL,
                value REAL NOT NULL,
                previous_value REAL,
                change_reason TEXT,
                notes TEXT,
                UNIQUE(timestamp, parameter_id)
            )
            ''')

            # コミットして閉じる
            conn.commit()
            conn.close()

            logger.info("データベース初期化成功")
            return True

        except Exception as e:
            logger.error(f"データベース初期化エラー: {e}")
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
            # JSONファイル読み込み
            with open(json_file, 'r') as f:
                data_list = json.load(f)

            if not isinstance(data_list, list):
                data_list = [data_list]  # リストでない場合は単一要素のリストに変換

            # データベース接続
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            total_inserted = 0

            # 各データ項目を処理
            for data in data_list:
                # タイムスタンプ抽出
                if 'timestamp' in data:
                    timestamp = data.get('datetime', str(
                        datetime.fromtimestamp(data['timestamp'])))
                else:
                    filename = os.path.basename(json_file)
                    match = re.search(r'_(\d{8})\.json$', filename)
                    date_str = match.group(
                        1) if match else datetime.now().strftime('%Y%m%d')
                    timestamp = f"{date_str}T12:00:00"

                # 日付と時間の抽出
                try:
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    date = dt.strftime('%Y-%m-%d')
                    time = dt.strftime('%H:%M:%S')
                except ValueError:
                    # タイムスタンプのフォーマットが異なる場合
                    dt = datetime.fromtimestamp(data['timestamp'])
                    date = dt.strftime('%Y-%m-%d')
                    time = dt.strftime('%H:%M:%S')

                # パラメータデータの挿入
                if 'parameters' in data:
                    parameters = data['parameters']
                    for param_id, param_info in parameters.items():
                        param_name = param_info.get('name', '')
                        value = param_info.get('value', 0)
                        unit = param_info.get('unit', '')

                        # データ挿入
                        cursor.execute('''
                        INSERT OR REPLACE INTO measurements 
                        (timestamp, date, time, parameter_id, parameter_name, value, unit)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (timestamp, date, time, param_id, param_name, value, unit))
                        total_inserted += 1

            # コミットして閉じる
            conn.commit()
            conn.close()

            logger.info(
                f"JSONデータのインポート成功: {json_file} ({total_inserted} レコード)")
            return True

        except Exception as e:
            logger.error(f"JSONデータのインポートエラー: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return False

    def import_all_json_data(self, json_dir=None, file_pattern="data_*.json"):
        """
        指定ディレクトリにある全てのJSONファイルをインポートする

        Args:
            json_dir: JSONファイルのディレクトリ（指定がなければ標準データディレクトリ）
            file_pattern: インポートするファイルのパターン

        Returns:
            tuple: (成功件数, 失敗件数)
        """
        try:
            # JSONディレクトリの設定
            if json_dir is None:
                json_dir = os.path.join(
                    os.path.dirname(os.path.dirname(
                        os.path.abspath(__file__))),
                    self.settings.get('files', {}).get(
                        'data_directory', 'data')
                )

            # JSONファイルの検索
            json_files = glob.glob(os.path.join(json_dir, file_pattern))

            if not json_files:
                logger.warning(
                    f"インポートするJSONファイルが見つかりません: {os.path.join(json_dir, file_pattern)}")
                return (0, 0)

            # 各ファイルのインポート
            success_count = 0
            failed_count = 0

            for file in json_files:
                if self.import_json_data(file):
                    success_count += 1
                else:
                    failed_count += 1

            logger.info(
                f"JSONデータのインポート完了: 成功 {success_count} 件, 失敗 {failed_count} 件")
            return (success_count, failed_count)

        except Exception as e:
            logger.error(f"JSONデータの一括インポートエラー: {e}")
            return (0, 0)


# スタンドアロン実行時のテスト用コード
if __name__ == "__main__":
    # コマンドライン引数の解析
    import argparse

    parser = argparse.ArgumentParser(description='LVYUANソーラーデータベース管理ツール')
    parser.add_argument('--init', action='store_true', help='データベースを初期化する')
    parser.add_argument('--import', dest='import_file',
                        help='指定したJSONファイルをインポートする')
    parser.add_argument('--import-all', action='store_true',
                        help='全てのJSONファイルをインポートする')
    parser.add_argument('--pattern', default="data_*.json",
                        help='インポートするJSONファイルのパターン（デフォルト: data_*.json）')
    parser.add_argument('--verbose', '-v',
                        action='store_true', help='詳細なログを出力する')

    args = parser.parse_args()

    # ロギングレベル設定
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    # データベースマネージャーの初期化
    db_manager = DatabaseManager()

    # コマンド実行
    if args.init:
        db_manager.init_db()

    if args.import_file:
        db_manager.import_json_data(args.import_file)

    if args.import_all:
        db_manager.import_all_json_data(file_pattern=args.pattern)

    # コマンドが指定されていない場合は初期化のみ行う
    if not (args.init or args.import_file or args.import_all):
        db_manager.init_db()
