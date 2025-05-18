#!/usr/bin/env python3
from email_notifier import EmailNotifier

# EmailNotifierインスタンスを作成
notifier = EmailNotifier()

# 日次レポートを送信
print("メールテストを実行します...")
result = notifier.send_daily_report()
print(f"メール送信結果: {'成功' if result else '失敗'}")
