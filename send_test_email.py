#!/usr/bin/env python3
"""
HANAZONOメールハブ v3.0 実メール送信テスト
"""

import sys
sys.path.append('.')
from email_hub_core import EmailHubCore

def main():
    print("📧 HANAZONOメールハブ v3.0 実メール送信テスト")
    
    hub = EmailHubCore()
    
    print("🔄 日次レポート送信実行中...")
    success = hub.run_daily_report()
    
    if success:
        print("✅ メール送信成功！受信トレイを確認してください")
    else:
        print("❌ メール送信失敗")

if __name__ == "__main__":
    main()
