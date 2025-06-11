#!/usr/bin/env python3
"""
HANAZONOメールハブ v3.0 メール内容プレビュー
実際の送信前に内容確認
"""

import sys
sys.path.append('.')
from email_hub_core import EmailHubCore

def main():
    print("📧 HANAZONOメールハブ v3.0 メール内容プレビュー")
    print("=" * 80)
    
    # ハブ初期化
    hub = EmailHubCore()
    
    # 設定読み込み
    if not hub.load_config():
        print("❌ 設定読み込み失敗")
        return
    
    # モジュール読み込み
    active_modules = hub.config.get('active_modules', [])
    for module_name in active_modules:
        hub.load_module(module_name)
    
    # レポート生成
    print("🔄 レポート生成中...")
    report_body = hub.generate_report("daily")
    
    print("\n📧 生成されたメール内容:")
    print("=" * 80)
    print(report_body)
    print("=" * 80)
    
    print(f"\n📊 文字数: {len(report_body)} 文字")
    print("📋 セクション数:", report_body.count("━━━"))

if __name__ == "__main__":
    main()
