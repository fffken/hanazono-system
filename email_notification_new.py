import os
import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

class EmailNotifier:

    def __init__(self, email_config):
        self.email_config = email_config

    def find_latest_data_file(self, target_date_str=None, data_dir='data'):
        """
        指定した日付のデータファイルを検索し、見つからない場合は
        利用可能な最新のデータファイルを返す

        Args:
            target_date_str: 検索する日付（YYYYMMDD形式、Noneなら前日）
            data_dir: データファイルの保存ディレクトリ

        Returns:
            最新のデータファイルパスとその日付、またはNoneとNone
        """
        if target_date_str is None:
            yesterday = datetime.now() - timedelta(days=1)
            target_date_str = yesterday.strftime('%Y%m%d')
        target_file = os.path.join(data_dir, f'lvyuan_data_{target_date_str}.csv')
        if os.path.exists(target_file):
            print(f'指定日付 {target_date_str} のデータファイルを使用します: {target_file}')
            return (target_file, target_date_str)
        print(f'指定日付 {target_date_str} のデータファイルが見つかりません。他の日付を検索します。')
        data_files = []
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.startswith('lvyuan_data_') and file.endswith('.csv'):
                    try:
                        date_str = file.split('_')[2].split('.')[0]
                        if len(date_str) == 8 and date_str.isdigit():
                            data_files.append((file, date_str))
                    except (IndexError, ValueError):
                        continue
        if data_files:
            data_files.sort(key=lambda x: x[1], reverse=True)
            latest_file = os.path.join(data_dir, data_files[0][0])
            latest_date = data_files[0][1]
            print(f'最新のデータファイルを発見: {latest_file} (日付: {latest_date})')
            return (latest_file, latest_date)
        print('利用可能なデータファイルが見つかりませんでした。')
        return (None, None)

    def format_date_jp(self, date_str):
        """日付を日本語形式にフォーマットする"""
        return f'{date_str[:4]}年{date_str[4:6]}月{date_str[6:8]}日'

    def send_daily_report(self):
        """日次レポートを送信する"""
        try:
            yesterday = datetime.now() - timedelta(days=1)
            yesterday_str = yesterday.strftime('%Y%m%d')
            data_file, actual_date_str = self.find_latest_data_file(yesterday_str)
            if data_file is None:
                print('利用可能なデータファイルが見つかりません。レポート送信をスキップします。')
                return False
            use_fallback = actual_date_str != yesterday_str
            if use_fallback:
                print(f'指定された日付 {yesterday_str} のデータがないため、日付 {actual_date_str} のデータを使用します')
            formatted_date = self.format_date_jp(actual_date_str)
            subject = f'🟡 LVYUANソーラー日次レポート {formatted_date}'
            if use_fallback:
                subject = f'⚠️ LVYUANソーラー日次レポート {formatted_date} (最新データ使用)'
            print(f'日次レポートを正常に送信しました。使用データ: {actual_date_str}')
            return True
        except Exception as e:
            print(f'日次レポート送信中にエラーが発生しました: {str(e)}')
            import traceback
            print(traceback.format_exc())
            return False