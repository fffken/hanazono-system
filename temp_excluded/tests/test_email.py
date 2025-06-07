from email_notifier import EmailNotifier
notifier = EmailNotifier()
print('メールテストを実行します...')
result = notifier.send_daily_report()
print(f"メール送信結果: {('成功' if result else '失敗')}")