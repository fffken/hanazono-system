import re
new_function = '\n    def send_daily_report(self, date=None):\n        """日次レポートを送信する"""\n        try:\n            # メール設定の確認\n            if "email" not in self.settings or not self.settings["email"].get("smtp_server"):\n                self.logger.error("メール設定が不足しています")\n                return False\n\n            # 日付の設定\n            if date is None:\n                yesterday = datetime.now() - timedelta(days=1)\n                date = yesterday.strftime("%Y%m%d")\n\n            # データファイルを探す（ない場合は最新のものを使用）\n            data_file, actual_date = self.find_latest_data_file(date)\n            if data_file is None:\n                self.logger.warning(f"日付 {date} のデータが見つかりません")\n                return False\n\n            # 日付が異なる場合は通知\n            use_fallback = (actual_date != date)\n            if use_fallback:\n                self.logger.warning(f"指定された日付 {date} のデータがないため、日付 {actual_date} のデータを使用します")\n'
subject_code = '\n            subject = f"🟡 LVYUANソーラー日次レポート {self._format_date_jp(actual_date)}"\n            if use_fallback:\n                subject = f"⚠️ LVYUANソーラー日次レポート {self._format_date_jp(actual_date)} (最新データ使用)"\n'
with open('email_notifier.py', 'r') as f:
    content = f.read()
send_daily_pattern = 'def send_daily_report\\([^)]*\\):.*?try:'
modified_content = re.sub(send_daily_pattern, new_function, content, flags=re.DOTALL)
subject_pattern = 'subject = .*?LVYUANソーラー日次レポート.*'
modified_content = re.sub(subject_pattern, subject_code, modified_content, flags=re.DOTALL)
with open('email_notifier.py', 'w') as f:
    f.write(modified_content)
print('send_daily_report関数を修正しました')