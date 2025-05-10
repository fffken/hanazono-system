#!/usr/bin/env python3
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
# from modules.database import DatabaseManager # データベースモジュールをインポート
from email.utils import formatdate
from logger_util import setup_logger

# ファイルスコープでロガーインスタンスを保持する変数
# setup_loggerはシングルトン的に振る舞うため、ここで一度取得すればどこでも同じインスタンスが使える
# main() 関数内で引数付きで再度呼び出すことでログレベルを制御する
_hanazono_logger_instance = setup_logger() # デフォルトはlogging.INFO

# Example log messages (テスト用なので、動作確認後に削除またはコメントアウトしても構いません)
# ロガー初期化直後のテストログは、main()関数内で設定レベルを調整した後に移動するのがより適切
# _hanazono_logger_instance.info("HANAZONOシステムを開始します。")
# _hanazono_logger_instance.warning("バッテリー残量が低下しています。")
try:
  # 例えば、ファイルが存在しない場合のエラーをシミュレート
  # with open("non_existent_file.txt", "r") as f:
  #  content = f.read()
  pass # 今は何もしない
except FileNotFoundError:
  # エラー発生時のログ出力も、ロガーが完全にセットアップされた後に行うのが望ましい
  # _hanazono_logger_instance.error("設定ファイルが見つかりません。", exc_info=True)
  pass # エラーハンドリングはmain()関数内で適切に行う

def collect_data():
  """データ収集処理"""
  # ファイルスコープのロガーインスタンスを使用
  logger = _hanazono_logger_instance
  if logger is None: # 念のためのチェック（通常はありえない）
    print("Error: Logger not initialized in collect_data")
    return None

  logger.info("データ収集開始")

  collector = LVYUANCollector()
  data, ip_changed = collector.collect_data()

  if data:
    logger.info(f"データ収集成功: {len(data['parameters'])} パラメーター")

    # IPアドレスが変更された場合は通知メール送信
    if ip_changed:
      old_ip = collector.settings["inverter"]["ip"]
      new_ip = data["ip_address"]

      logger.info(f"インバーターIPアドレス変更検出: {old_ip} → {new_ip}")

      # メール通知
      notifier = EmailNotifier()
      if notifier.send_ip_change_notification(old_ip, new_ip):
        logger.info("IPアドレス変更通知メール送信成功")
      else:
        logger.warning("IPアドレス変更通知メール送信失敗")
  else:
    logger.error("データ収集失敗")

  return data is not None

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
  # ファイルスコープのロガーインスタンスを使用
  logger = _hanazono_logger_instance
  if logger is None: # 念のためのチェック
    print("Error: Logger not initialized in send_daily_report")
    return False
  logger.info("日次レポート送信を開始します")

  # メール通知クラスの初期化
  notifier = EmailNotifier()

  # 設定ファイルの読み込み（エラーハンドリング強化）
  settings = {}
  settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json')
  try:
    with open(settings_file, 'r') as f:
      settings = json.load(f)
    logger.info("設定ファイル読み込み成功")
  except FileNotFoundError:
    logger.error(f"設定ファイルが見つかりません: {settings_file}")
  except json.JSONDecodeError as e:
    logger.error(f"設定ファイル形式エラー: {e}")
  except Exception as e:
    logger.error(f"設定ファイル読み込みエラー: {e}")

  # 日付計算（フォーマットを設定ファイルから読み込み）
  date_format = settings.get('files', {}).get('date_format', '%Y%m%d')
  yesterday = (datetime.now() - timedelta(days=1)).strftime(date_format)
  today = datetime.now().strftime(date_format)

  # データディレクトリの設定
  data_dir = settings.get('files', {}).get('data_directory', 'data')
  if not os.path.exists(data_dir):
    os.makedirs(data_dir, exist_ok=True)
    logger.info(f"データディレクトリを作成しました: {data_dir}")

  # ファイルプレフィックス設定
  file_prefix = settings.get('files', {}).get('data_prefix', 'data_')

  # データファイルの検索パターン
  data_file_patterns = [
    os.path.join(data_dir, f"{file_prefix}{yesterday}*.json"),
    os.path.join(data_dir, f"{file_prefix}{today}*.json")
  ]

  # 前日データの確認
  yesterday_files = sorted(glob.glob(data_file_patterns[0]), reverse=True)
  if yesterday_files:
    # 前日データが存在する場合
    logger.info(f"前日({yesterday})のデータを使用してレポート生成します: {yesterday_files[0]}")
    # send_daily_reportメソッドにファイルパスではなく日付文字列を渡しているか確認
    return notifier.send_daily_report(yesterday)

  # 当日データの確認
  today_files = sorted(glob.glob(data_file_patterns[1]), reverse=True)
  if today_files:
    # 当日データが存在する場合
    logger.warning(f"前日データなし。当日({today})のデータを使用します: {today_files[0]}")
    notifier.append_note(f"前日データがないため、当日({today})のデータを使用しています")
    # send_daily_reportメソッドにファイルパスではなく日付文字列を渡しているか確認
    return notifier.send_daily_report(today)

  # 前日・当日データがどちらもない場合は、最新のデータファイルを探す
  all_data_files = glob.glob(os.path.join(data_dir, f"{file_prefix}*.json"))
  if all_data_files:
    # 正規表現パターンをファイルプレフィックスから動的に生成
    date_pattern = re.compile(f'{re.escape(file_prefix)}(\\d{{8}})')
    dated_files = []

    for file_path in all_data_files:
      file_name = os.path.basename(file_path)
      match = date_pattern.search(file_name)
      if match:
        date_str = match.group(1)
        dated_files.append((file_path, date_str))

      # 日付でソート（最新順）
      dated_files.sort(key=lambda x: x[1], reverse=True)
      newest_file = dated_files[0][0]
      file_date = dated_files[0][1]
      logger.warning(f"近日データなし。最新データ({file_date})を使用します: {newest_file}")
      notifier.append_note(f"最近のデータがないため、{file_date}のデータを使用しています")
      # send_daily_reportメソッドにファイルパスではなく日付文字列を渡しているか確認
      return notifier.send_daily_report(file_date)


  # データが全くない場合
  logger.error("レポート用データが見つかりません。レポート送信をスキップします")
  # send_alertはnotifierインスタンスのメソッドとして呼び出す
  notifier.send_alert("データファイル欠損", "レポート生成に必要なデータが見つかりません")
  return False

def check_cron_job():
  """cronジョブの確認と設定"""
  # ファイルスコープのロガーインスタンスを使用
  logger = _hanazono_logger_instance
  if logger is None: # 念のためのチェック
    print("Error: Logger not initialized in check_cron_job")
    return False

  import subprocess

  try:
    # 現在のcronジョブ確認
    result = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    current_crontab = result.stdout

    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, 'main.py')

    # 必要なcronジョブ
    cron_jobs = [
      f"*/15 * * * * cd {script_dir} && python3 {main_script} --collect > /dev/null 2>&1", # 15分ごとのデータ収集
      f"0 8 * * * cd {script_dir} && python3 {main_script} --daily-report > /dev/null 2>&1" # 毎朝8時の日次レポート送信
    ]

    # 既存のジョブ確認
    missing_jobs = []
    for job in cron_jobs:
      if job not in current_crontab:
        missing_jobs.append(job)

    # 不足ジョブがあれば追加
    if missing_jobs:
      logger.info("必要なcronジョブを追加します")

      # 既存のジョブと新規ジョブを結合
      new_crontab = current_crontab.strip() + "\n"
      if new_crontab == "\n": # 空の場合
        new_crontab = ""

      for job in missing_jobs:
        new_crontab += job + "\n"

      # 一時ファイルに書き出し
      temp_file = "/tmp/new_crontab.txt"
      with open(temp_file, 'w') as f:
        f.write(new_crontab)

      # crontabに設定
      subprocess.run(['crontab', temp_file])

      logger.info("cronジョブ設定完了")
    else:
      logger.info("必要なcronジョブは既に設定されています")

    return True

  except Exception as e:
    logger.error(f"cronジョブ設定エラー: {e}")
    return False


def main():
  """メイン処理"""
  # 引数解析
  parser = argparse.ArgumentParser(description='HANAZONOシステム自動最適化')
  parser.add_argument('--collect', action='store_true', help='データ収集を実行')
  parser.add_argument('--daily-report', action='store_true', help='日次レポートを送信')
  parser.add_argument('--setup', action='store_true', help='初期設定（cronジョブ登録など）を実行')
  parser.add_argument('--db-init', action='store_true', help='データベースを初期化')
  parser.add_argument('--db-import', action='store_true', help='JSONデータをデータベースにインポート')
  parser.add_argument('--debug', action='store_true', help='デバッグモードで実行')

  args = parser.parse_args()

  # ロギング設定 (main()関数内で引数付きで呼び出すことで、コマンドライン引数でログレベルを制御)
  log_level = logging.DEBUG if args.debug else logging.INFO

  # setup_logger はシングルトン的に振る舞うため、ここで取得すればどこでも同じインスタンスが使える
  # ファイルスコープの _hanazono_logger_instance のレベルを更新する
  global _hanazono_logger_instance
  _hanazono_logger_instance = setup_logger(log_level)

  # main 関数内のログ出力は、ここで設定したロガーインスタンスを使用
  _hanazono_logger_instance.info("HANAZONOシステム自動最適化を開始します")

  # ファイル冒頭のテスト用ログ出力をここに移動するか削除
  # 例: _hanazono_logger_instance.info("HANAZONOシステムを開始します。")

  try:
    # データ収集
    if args.collect:
      collect_data()

    # 日次レポート送信
    if args.daily_report:
      send_daily_report()

    # 初期設定
    if args.setup:
      check_cron_job()

      # 初回データ収集
      collect_data()
    # データベース初期化
    if args.db_init:
      # DatabaseManager クラスが modules/database.py に存在する必要があります
      try:
        from modules.database import DatabaseManager
      except ImportError:
        _hanazono_logger_instance.error("DatabaseManager モジュールが見つかりません。データベース機能はスキップされます。")
        return # または sys.exit(1)

      db_manager = DatabaseManager()
      if db_manager.init_db():
        _hanazono_logger_instance.info("データベース初期化が完了しました")
      else:
        _hanazono_logger_instance.error("データベース初期化に失敗しました")

    # JSONデータのインポート
    if args.db_import:
      # DatabaseManager クラスが modules/database.py に存在する必要があります
      try:
        from modules.database import DatabaseManager
      except ImportError:
        _hanazono_logger_instance.error("DatabaseManager モジュールが見つかりません。データベース機能はスキップされます。")
        return # または sys.exit(1)

      db_manager = DatabaseManager()
      success, failed = db_manager.import_all_json_data()
      _hanazono_logger_instance.info(f"データインポート結果: 成功 {success} 件, 失敗 {failed} 件")

    # 引数指定なし
    if not any([args.collect, args.daily_report, args.setup, args.db_init, args.db_import]):
      parser.print_help()

  except Exception as e:
    _hanazono_logger_instance.error(f"実行エラー: {e}", exc_info=True)

  _hanazono_logger_instance.info("HANAZONOシステム自動最適化を終了します")

if __name__ == "__main__":
  main()
