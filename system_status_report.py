#!/usr/bin/env python3
"""
System Status Report Script
目的: 稼働中・停止中システム確認、HCQASシステム・メール機能現状レポート
原則: 読み取り専用・非破壊的・即座削除対象
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def check_running_processes():
    """現在稼働中のプロセス確認"""
    print("🔍 稼働中プロセス確認...")
    
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        relevant_processes = []
        
        for line in result.stdout.splitlines():
            if any(keyword in line.lower() for keyword in 
                  ['python', 'collector', 'lvyuan', 'cron', 'email', 'hcqas']):
                if not any(exclude in line for exclude in ['grep', 'nano', 'system_status_report']):
                    relevant_processes.append(line.strip())
        
        if relevant_processes:
            print("📊 関連プロセス:")
            for proc in relevant_processes[:10]:  # 最初の10個
                print(f"   {proc}")
        else:
            print("📊 関連プロセスなし")
            
    except Exception as e:
        print(f"❌ プロセス確認エラー: {e}")

def check_cron_status():
    """cron稼働状況確認"""
    print("⏰ cron稼働状況確認...")
    
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            active_jobs = [line for line in result.stdout.splitlines() 
                          if line.strip() and not line.startswith('#')]
            print(f"📋 アクティブなcronジョブ: {len(active_jobs)}個")
            for job in active_jobs:
                print(f"   - {job}")
        else:
            print("❌ cron設定なし")
    except Exception as e:
        print(f"❌ cron確認エラー: {e}")

def check_security_system():
    """セキュリティシステム状況"""
    print("🛡️ セキュリティシステム状況...")
    
    security_path = Path("security_clearance")
    if security_path.exists():
        certs = list(Path("security_clearance/certificates").glob("*.json"))
        tickets = list(Path("security_clearance/execution_tickets").glob("*.json"))
        quarantine = list(Path("security_clearance/quarantine").glob("*"))
        
        print(f"📋 セキュリティ証明書: {len(certs)}個")
        print(f"🎫 アクティブチケット: {len(tickets)}個")
        print(f"🔒 隔離スクリプト: {len(quarantine)}個")
        print("✅ セキュリティシステム: 稼働中")
    else:
        print("❌ セキュリティシステム: 未構築")

def check_automation_recovery():
    """自動化復旧状況"""
    print("🔄 自動化スクリプト復旧状況...")
    
    if Path("automation_emergency_control.json").exists():
        with open("automation_emergency_control.json", 'r') as f:
            data = json.load(f)
        
        disabled_scripts = data.get("disabled_scripts", [])
        recovered = []
        
        for script_info in disabled_scripts:
            original = script_info["original"]
            if Path(original).exists():
                recovered.append(original)
        
        print(f"📊 総無効化スクリプト: {len(disabled_scripts)}個")
        print(f"✅ 復旧済み: {len(recovered)}個")
        print(f"⏳ 未復旧: {len(disabled_scripts) - len(recovered)}個")
        
        if recovered:
            print("📋 復旧済みスクリプト:")
            for script in recovered:
                print(f"   - {script}")
    else:
        print("❌ 自動化制御データなし")

def check_hcqas_system():
    """HCQASシステム現状確認"""
    print("🧠 HCQASシステム現状確認...")
    
    hcqas_files = [
        "hcqas_capsule.py",
        "hcqas_implementation/",
        "HCQAS.md"
    ]
    
    hcqas_status = {"files_exist": [], "missing": []}
    
    for item in hcqas_files:
        if Path(item).exists():
            hcqas_status["files_exist"].append(item)
            if item == "hcqas_capsule.py":
                try:
                    with open(item, 'r') as f:
                        content = f.read()
                    print(f"✅ {item}: 存在 ({len(content)}文字)")
                except:
                    print(f"⚠️ {item}: 存在するが読み取り不可")
            else:
                print(f"✅ {item}: 存在")
        else:
            hcqas_status["missing"].append(item)
            print(f"❌ {item}: 不存在")
    
    # HCQAS動作テスト
    if "hcqas_capsule.py" in hcqas_status["files_exist"]:
        print("🧪 HCQAS動作テスト...")
        try:
            result = subprocess.run(['python3', 'hcqas_capsule.py'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ HCQAS: 動作正常")
            else:
                print(f"⚠️ HCQAS: エラー - {result.stderr[:100]}")
        except subprocess.TimeoutExpired:
            print("⚠️ HCQAS: タイムアウト")
        except Exception as e:
            print(f"⚠️ HCQAS: テストエラー - {e}")

def check_email_system():
    """メールシステム現状確認"""
    print("📧 メールシステム現状確認...")
    
    email_files = [
        "main.py",
        "email_capsule.py", 
        "email_notifier_v2_1.py",
        "settings.json"
    ]
    
    email_status = {"files_exist": [], "missing": []}
    
    for item in email_files:
        if Path(item).exists():
            email_status["files_exist"].append(item)
            print(f"✅ {item}: 存在")
        else:
            email_status["missing"].append(item)
            print(f"❌ {item}: 不存在")
    
    # メイン機能テスト
    if "main.py" in email_status["files_exist"]:
        print("🧪 メイン機能確認...")
        try:
            result = subprocess.run(['python3', 'main.py', '--help'], 
                                  capture_output=True, text=True, timeout=5)
            if "daily-report" in result.stdout:
                print("✅ メイン機能: daily-report対応")
            else:
                print("⚠️ メイン機能: 不明")
        except Exception as e:
            print(f"⚠️ メイン機能: テストエラー - {e}")
    
    # email_capsule動作確認
    if "email_capsule.py" in email_status["files_exist"]:
        print("🧪 email_capsule動作確認...")
        try:
            with open("email_capsule.py", 'r') as f:
                content = f.read()
            if "smtp" in content.lower():
                print("✅ email_capsule: SMTP設定あり")
            else:
                print("⚠️ email_capsule: SMTP設定不明")
        except Exception as e:
            print(f"⚠️ email_capsule: 確認エラー - {e}")

def check_data_collection():
    """データ収集システム確認"""
    print("📊 データ収集システム確認...")
    
    collection_files = [
        "collector_capsule.py",
        "lvyuan_collector.py"
    ]
    
    for item in collection_files:
        if Path(item).exists():
            print(f"✅ {item}: 存在")
        else:
            print(f"❌ {item}: 不存在")
    
    # 最近のデータ確認
    data_dir = Path("data")
    if data_dir.exists():
        recent_files = sorted(data_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
        if recent_files:
            latest = recent_files[0]
            mod_time = datetime.fromtimestamp(latest.stat().st_mtime)
            print(f"📊 最新データ: {latest.name} ({mod_time.strftime('%Y-%m-%d %H:%M')})")
        else:
            print("⚠️ データファイルなし")
    else:
        print("❌ dataディレクトリなし")

def main():
    print("📊 システム全体現状レポート")
    print(f"実行時刻: {datetime.now()}")
    
    print_section("稼働中システム確認")
    check_running_processes()
    check_cron_status()
    
    print_section("セキュリティ・自動化状況")
    check_security_system()
    check_automation_recovery()
    
    print_section("HCQASシステム現状")
    check_hcqas_system()
    
    print_section("メールシステム現状")
    check_email_system()
    
    print_section("データ収集システム現状")
    check_data_collection()
    
    print_section("🎯 総合レポート完了")
    print("📋 システム全体の現状確認が完了しました")
    print("⚡ 次アクション推奨: 問題箇所の優先度付け・改善計画策定")

if __name__ == "__main__":
    main()
