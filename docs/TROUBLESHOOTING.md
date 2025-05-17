# HANAZONOシステム トラブルシューティング

## よくあるエラーパターンと解決策

### 1. メール送信エラー

#### 症状: [SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:992)
- **原因**: SMTPポート設定またはSTARTTLS設定の問題
- **解決策**:
  ```python
  # SMTP_SSLではなく、SMTPを使用しSTARTTLSを有効化
  server = smtplib.SMTP(smtp_server, smtp_port)
  server.starttls()
