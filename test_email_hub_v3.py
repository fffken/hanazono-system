#!/usr/bin/env python3
"""
HANAZONOメールハブ v3.0 基本テスト診断スクリプト
非破壊的テスト・バックアップ・依存関係確認
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


def print_section(title):
    """セクション表示"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)


def backup_existing_files():
    """既存ファイルバックアップ"""
    print_section("既存ファイルバックアップ作成")
    
    backup_dir = f"backup_email_system_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    files_to_backup = [
        "email_notifier_v2_1.py",
        "settings.json",
        "main.py"
    ]
    
    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy2(file, f"{backup_dir}/{file}")
            print(f"✅ バックアップ完了: {file} → {backup_dir}/")
        else:
            print(f"⚠️  ファイル未存在: {file}")
    
    print(f"📁 バックアップディレクトリ: {backup_dir}")
    return backup_dir


def check_dependencies():
    """依存関係確認"""
    print_section("依存関係チェック")
    
    required_modules = [
        "pysolarmanv5",
        "requests",
        "json",
        "smtplib",
        "email"
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            if module in ["json", "smtplib", "email"]:
                # 標準ライブラリ
                __import__(module)
                print(f"✅ {module}: OK (標準ライブラリ)")
            else:
                __import__(module)
                print(f"✅ {module}: OK")
        except ImportError:
            print(f"❌ {module}: 未インストール")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n🚨 未インストールモジュール: {', '.join(missing_modules)}")
        print("📦 インストールコマンド:")
        for module in missing_modules:
            print(f"   pip3 install {module}")
        return False
    else:
        print("\n✅ 全依存関係OK")
        return True


def check_config_file():
    """設定ファイル確認"""
    print_section("設定ファイル確認")
    
    config_path = "hub_config.json"
    
    if not os.path.exists(config_path):
        print(f"❌ 設定ファイル未存在: {config_path}")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"✅ 設定ファイル読み込み成功: {config_path}")
        
        # 必須設定確認
        required_sections = ["email", "active_modules", "system"]
        for section in required_sections:
            if section in config:
                print(f"✅ {section}セクション: OK")
            else:
                print(f"❌ {section}セクション: 未設定")
                return False
        
        # SMTP設定詳細確認
        email_config = config.get("email", {})
        smtp_fields = ["smtp_server", "smtp_port", "sender_email", "receiver_email", "sender_password"]
        
        print("\n📧 SMTP設定確認:")
        for field in smtp_fields:
            if field in email_config and email_config[field]:
                if field == "sender_password":
                    print(f"✅ {field}: ******* (設定済み)")
                else:
                    print(f"✅ {field}: {email_config[field]}")
            else:
                print(f"❌ {field}: 未設定")
                return False
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析エラー: {e}")
        return False
    except Exception as e:
        print(f"❌ 設定ファイルエラー: {e}")
        return False


def check_module_files():
    """モジュールファイル確認"""
    print_section("モジュールファイル確認")
    
    module_dir = "modules"
    required_modules = [
        "__init__.py",
        "battery_module.py", 
        "weather_module.py",
        "news_module.py"
    ]
    
    if not os.path.exists(module_dir):
        print(f"❌ モジュールディレクトリ未存在: {module_dir}")
        return False
    
    for module in required_modules:
        module_path = f"{module_dir}/{module}"
        if os.path.exists(module_path):
            print(f"✅ {module}: 存在")
        else:
            print(f"❌ {module}: 未存在")
            return False
    
    return True


def test_basic_import():
    """基本インポートテスト"""
    print_section("基本インポートテスト")
    
    try:
        # email_hub_coreのインポートテスト
        sys.path.append('.')
        import email_hub_core
        print("✅ email_hub_core.py: インポート成功")
        
        # EmailHubCoreクラステスト
        hub = email_hub_core.EmailHubCore()
        print("✅ EmailHubCoreクラス: 初期化成功")
        
        return True
        
    except Exception as e:
        print(f"❌ インポートエラー: {e}")
        return False


def test_config_loading():
    """設定読み込みテスト"""
    print_section("設定読み込みテスト")
    
    try:
        sys.path.append('.')
        import email_hub_core
        
        hub = email_hub_core.EmailHubCore()
        success = hub.load_config()
        
        if success:
            print("✅ 設定読み込み: 成功")
            print(f"📊 アクティブモジュール: {hub.config.get('active_modules', [])}")
            return True
        else:
            print("❌ 設定読み込み: 失敗")
            return False
            
    except Exception as e:
        print(f"❌ 設定読み込みエラー: {e}")
        return False


def test_module_loading():
    """モジュール読み込みテスト"""
    print_section("モジュール読み込みテスト")
    
    try:
        sys.path.append('.')
        import email_hub_core
        
        hub = email_hub_core.EmailHubCore()
        hub.load_config()
        
        # モジュール読み込みテスト
        test_modules = ["battery_module", "weather_module", "news_module"]
        
        for module_name in test_modules:
            success = hub.load_module(module_name)
            if success:
                print(f"✅ {module_name}: 読み込み成功")
            else:
                print(f"❌ {module_name}: 読み込み失敗")
        
        return True
        
    except Exception as e:
        print(f"❌ モジュール読み込みエラー: {e}")
        return False


def run_complete_test():
    """完全テスト実行"""
    print("🚀 HANAZONOメールハブ v3.0 基本テスト開始")
    print(f"📅 テスト実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # テスト項目
    tests = [
        ("バックアップ作成", backup_existing_files),
        ("依存関係チェック", check_dependencies),
        ("設定ファイル確認", check_config_file),
        ("モジュールファイル確認", check_module_files),
        ("基本インポートテスト", test_basic_import),
        ("設定読み込みテスト", test_config_loading),
        ("モジュール読み込みテスト", test_module_loading)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if test_name == "バックアップ作成":
                backup_dir = test_func()
                results.append((test_name, True, backup_dir))
            else:
                result = test_func()
                results.append((test_name, result, None))
        except Exception as e:
            print(f"❌ {test_name} 実行エラー: {e}")
            results.append((test_name, False, str(e)))
    
    # 結果サマリー
    print_section("テスト結果サマリー")
    
    success_count = 0
    for test_name, success, extra in results:
        if success:
            print(f"✅ {test_name}: 成功")
            success_count += 1
        else:
            print(f"❌ {test_name}: 失敗")
            if extra:
                print(f"   詳細: {extra}")
    
    print(f"\n📊 テスト結果: {success_count}/{len(results)} 成功")
    
    if success_count == len(results):
        print("🎉 全テスト成功！メールハブv3.0準備完了")
        return True
    else:
        print("🚨 一部テスト失敗。問題解決が必要です。")
        return False


if __name__ == "__main__":
    try:
        success = run_complete_test()
        if success:
            print("\n🚀 次のステップ: 実際のメール送信テストが可能です")
        else:
            print("\n🔧 修復作業が必要です")
    except KeyboardInterrupt:
        print("\n⏹️  テスト中断")
    except Exception as e:
        print(f"\n💥 予期しないエラー: {e}")
