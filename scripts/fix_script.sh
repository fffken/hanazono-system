#!/bin/bash

# バックアップ作成
cp email_notifier.py email_notifier.py.backup.autofix.$(date +%Y%m%d%H%M%S)

# 1064行前後の状態確認
echo "修正前の1064行周辺:"
sed -n '1060,1068p' email_notifier.py

# 1064行から1088行までを含む範囲を特定し、置換するファイルを作成
cat > /tmp/replacement.py << 'EOF'
    def send_alert(self, subject, message, to_email=None):
        """
        アラートメールを送信する

        Args:
            subject: アラート件名
            message: アラートメッセージ
            to_email: 送信先(省略時は設定から取得)

        Returns:
            bool: 送信成功ならTrue
        """
        # 件名にアラートプレフィックスを追加
        subject = f"🚨 {subject}"
        body = f"【アラート】\n\n{message}\n\n発生時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        self.logger.info(f"アラートメール送信: {subject}")

        return self._send_email(
            to_email=to_email,
            subject=subject,
            body_text=body,
            body_html=f"<html><body><p>{body}</p></body></html>"
        )
EOF

# 1064行から1088行までを置換
# まず削除してから挿入
sed -i '1064,1088d' email_notifier.py
sed -i '1063a\\' email_notifier.py  # 空行を挿入
sed -i "1064r /tmp/replacement.py" email_notifier.py

echo "修正後の1064行周辺:"
sed -n '1060,1068p' email_notifier.py

echo "修正完了。テストを実行してください。"
