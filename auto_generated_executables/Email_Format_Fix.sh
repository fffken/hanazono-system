#!/bin/bash

echo "📧 メール形式修正開始..."

# email_notifier.pyのメール送信部分を修正
python3 << 'PYTHON_FORMAT_FIX'
with open('email_notifier.py', 'r') as f:
    content = f.read()

# HTMLメール送信をテキストメール送信に変更
content = content.replace(
    "msg.attach(MIMEText(text_content, 'html', 'utf-8'))",
    "msg.attach(MIMEText(text_content, 'plain', 'utf-8'))"
)

with open('email_notifier.py', 'w') as f:
    f.write(content)

print("✅ メール形式をHTMLからテキストに変更")
PYTHON_FORMAT_FIX

echo "✅ メール形式修正完了"

