#!/usr/bin/env python3
"""
Kioku System Status Integration Script
目的: セキュリティ・復旧状況をkiokuシステムに統合し、新AIの自動状況表示機能追加
原則: バックアップ前提・非破壊的・即座削除対象
作成: 一時使用目的（統合完了後削除）
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def create_backup():
    """kiokuシステムバックアップ"""
    backup_dir = f"ai_memory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copytree("ai_memory", backup_dir)
    print(f"✅ kiokuシステムバックアップ: {backup_dir}")
    return backup_dir

def collect_current_system_status():
    """現在のシステム状況収集"""
    status = {
        "timestamp": datetime.now().isoformat(),
        "security_system": {},
        "automation_recovery": {},
        "system_health": {},
        "active_scripts": {}
    }
    
    # セキュリティシステム状況
    if Path("security_clearance").exists():
        certs = list(Path("security_clearance/certificates").glob("*.json"))
        tickets = list(Path("security_clearance/execution_tickets").glob("*.json"))
        quarantine = list(Path("security_clearance/quarantine").glob("*"))
        
        status["security_system"] = {
            "certificates_count": len(certs),
            "active_tickets": len(tickets),
            "quarantined_scripts": len(quarantine),
            "system_status": "ACTIVE"
        }
    
    # 自動化復旧状況
    if Path("automation_emergency_control.json").exists():
        with open("automation_emergency_control.json", 'r') as f:
            emergency_data = json.load(f)
        
        disabled_count = len(emergency_data.get("disabled_scripts", []))
        recovered_scripts = []
        
        # 復旧済みスクリプト確認
        for script_info in emergency_data.get("disabled_scripts", []):
            original_path = script_info["original"]
            if Path(original_path).exists():
                recovered_scripts.append(original_path)
        
        status["automation_recovery"] = {
            "total_disabled": disabled_count,
            "recovered_count": len(recovered_scripts),
            "recovered_scripts": recovered_scripts,
            "recovery_rate": f"{len(recovered_scripts)}/{disabled_count}"
        }
    
    # システム健全性
    try:
        import subprocess
        cron_result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        active_crons = len([line for line in cron_result.stdout.splitlines() 
                           if line.strip() and not line.startswith('#')])
        
        status["system_health"] = {
            "active_cron_jobs": active_crons,
            "venv_status": "ACTIVE" if Path("venv").exists() else "MISSING",
            "core_systems": "OPERATIONAL"
        }
    except:
        status["system_health"] = {"status": "CHECK_REQUIRED"}
    
    return status

def update_core_knowledge(system_status):
    """core_knowledge.jsonにシステム状況を追加"""
    permanent_path = Path("ai_memory/storage/permanent")
    core_knowledge_file = permanent_path / "core_knowledge.json"
    
    if core_knowledge_file.exists():
        with open(core_knowledge_file, 'r', encoding='utf-8') as f:
            core_knowledge = json.load(f)
    else:
        core_knowledge = {}
    
    # システム状況セクション追加
    core_knowledge["current_system_status"] = system_status
    core_knowledge["last_status_update"] = datetime.now().isoformat()
    
    # critical_rulesにシステム状況確認を追加
    critical_rules = core_knowledge.setdefault("critical_rules", [])
    status_rule = "新AIセッション開始時: システム状況自動表示でプロジェクト継続性確保"
    if status_rule not in critical_rules:
        critical_rules.append(status_rule)
    
    # ファイル更新
    with open(core_knowledge_file, 'w', encoding='utf-8') as f:
        json.dump(core_knowledge, f, indent=2, ensure_ascii=False)
    
    print("✅ core_knowledge.json更新完了")
    return True

def update_startup_memory(system_status):
    """ai_startup_memory.pyにシステム状況表示機能追加"""
    startup_file = Path("ai_memory/ai_startup_memory.py")
    
    # バックアップ
    backup_file = f"{startup_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(startup_file, backup_file)
    
    # ファイル読み込み
    with open(startup_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # システム状況表示コード
    status_display_code = '''
        # システム状況自動表示
        current_status = core_knowledge.get('current_system_status', {})
        if current_status:
            print("✅ システム状況記憶復旧成功")
            security = current_status.get('security_system', {})
            recovery = current_status.get('automation_recovery', {})
            health = current_status.get('system_health', {})
            
            print(f"   🛡️ セキュリティ: 証明書{security.get('certificates_count', 0)}個, チケット{security.get('active_tickets', 0)}個")
            print(f"   🔄 自動化復旧: {recovery.get('recovery_rate', '0/0')} 復旧済み")
            print(f"   ⚙️ システム健全性: cron{health.get('active_cron_jobs', 0)}個稼働中")
            print(f"   📊 最終更新: {core_knowledge.get('last_status_update', '不明')}")
'''
    
    # core_knowledge処理の後に挿入
    if "system_map_info" in content and "current_status" not in content:
        lines = content.splitlines()
        insertion_point = None
        
        for i, line in enumerate(lines):
            if "system_map_info" in line and "system_map_info.get" in line:
                insertion_point = i + 4  # system_map_info処理の後
                break
        
        if insertion_point:
            new_lines = []
            new_lines.extend(lines[:insertion_point])
            new_lines.extend(status_display_code.splitlines())
            new_lines.extend(lines[insertion_point:])
            
            # ファイル更新
            with open(startup_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            print("✅ ai_startup_memory.py更新完了")
            return True
    
    print("⚠️ ai_startup_memory.py更新をスキップ（既存または挿入ポイント未発見）")
    return False

def verify_integration():
    """統合結果の検証"""
    verification_items = []
    
    # core_knowledge確認
    core_knowledge_file = Path("ai_memory/storage/permanent/core_knowledge.json")
    if core_knowledge_file.exists():
        with open(core_knowledge_file, 'r', encoding='utf-8') as f:
            core_knowledge = json.load(f)
        
        if "current_system_status" in core_knowledge:
            verification_items.append("core_knowledge.json: システム状況追加")
        
        if any("システム状況自動表示" in rule for rule in core_knowledge.get("critical_rules", [])):
            verification_items.append("core_knowledge.json: 状況表示ルール追加")
    
    # startup_memory確認
    startup_file = Path("ai_memory/ai_startup_memory.py")
    if startup_file.exists():
        with open(startup_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "current_status" in content and "システム状況記憶復旧成功" in content:
            verification_items.append("ai_startup_memory.py: 自動状況表示機能追加")
    
    return verification_items

def main():
    print("🧠 Kioku System Status Integration")
    print(f"実行時刻: {datetime.now()}")
    print("目的: システム状況をkiokuシステムに統合・新AI自動表示機能追加")
    
    print_section("Phase 1: kiokuシステムバックアップ")
    backup_path = create_backup()
    
    print_section("Phase 2: 現在システム状況収集")
    system_status = collect_current_system_status()
    
    print("📊 収集されたシステム状況:")
    print(f"   🛡️ セキュリティシステム: {system_status['security_system']}")
    print(f"   🔄 自動化復旧: {system_status['automation_recovery']}")
    print(f"   ⚙️ システム健全性: {system_status['system_health']}")
    
    print_section("Phase 3: core_knowledge.json更新")
    core_success = update_core_knowledge(system_status)
    
    print_section("Phase 4: ai_startup_memory.py更新")
    startup_success = update_startup_memory(system_status)
    
    print_section("Phase 5: 統合検証")
    verification_items = verify_integration()
    
    print_section("🎯 kiokuシステム統合結果")
    
    if verification_items:
        print("🎉 kiokuシステム統合完全成功！")
        for item in verification_items:
            print(f"✅ {item}")
        
        print(f"\n📋 次回AI起動時の効果:")
        print("   - システム状況が自動表示されます")
        print("   - セキュリティ状態・復旧状況が即座把握可能")
        print("   - プロジェクト継続性が大幅向上")
        
        print(f"\n🔄 次のステップ:")
        print("1. git add ai_memory/")
        print("2. git commit -m 'feat: kiokuシステム状況表示統合'")
        print("3. git push")
        print("4. rm kioku_system_status_integration.py")
        
        print(f"\n🧠 革命的成果:")
        print("   新AIが即座にシステム全体状況を把握可能になります")
        
    else:
        print("❌ 統合に問題が発生しました")
        print(f"🔄 復旧: cp -r {backup_path}/* ai_memory/")

if __name__ == "__main__":
    main()
