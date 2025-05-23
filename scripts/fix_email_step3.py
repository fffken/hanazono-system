import re

# send_daily_report関数の修正部分
new_function = '''
    def send_daily_report(self, date=None):
        """日次レポートを送信する"""
        try:
            # メール設定の確認
            if "email" not in self.settings or not self.settings["email"].get("smtp_server"):
                self.logger.error("メール設定が不足しています")
                return False
                
            # 日付の設定
            if date is None:
                yesterday = datetime.now() - timedelta(days=1)
                date = yesterday.strftime("%Y%m%d")
                
            # データファイルを探す（ない場合は最新のものを使用）
            data_file, actual_date = self.find_latest_data_file(date)
            if data_file is None:
                self.logger.warning(f"日付 {date} のデータが見つかりません")
                return False
                
            # 日付が異なる場合は通知
            use_fallback = (actual_date != date)
            if use_fallback:
                self.logger.warning(f"指定された日付 {date} のデータがないため、日付 {actual_date} のデータを使用します")
'''

# 件名の修正部分
subject_code = '''
            subject = f"🟡 LVYUANソーラー日次レポート {self._format_date_jp(actual_date)}"
            if use_fallback:
                subject = f"⚠️ LVYUANソーラー日次レポート {self._format_date_jp(actual_date)} (最新データ使用)"
'''

# ファイル読み込み
with open('email_notifier.py', 'r') as f:
    content = f.read()

# send_daily_report関数を置換
send_daily_pattern = r'def send_daily_report\([^)]*\):.*?try:'
modified_content = re.sub(
    send_daily_pattern, new_function, content, flags=re.DOTALL)

# 件名設定の行を置換
subject_pattern = r'subject = .*?LVYUANソーラー日次レポート.*'
modified_content = re.sub(subject_pattern, subject_code,
                          modified_content, flags=re.DOTALL)

# 修正内容を保存
with open('email_notifier.py', 'w') as f:
    f.write(modified_content)

print("send_daily_report関数を修正しました")
