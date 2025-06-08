#!/usr/bin/env python3
"""
Kioku Permanent Memory Integration Script
目的: システムマップを固定記憶領域（permanent）に統合
原則: 永続化・次回AI必須継承・即座削除対象
作成: 一時使用目的（統合完了後削除）
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

def print_section(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def backup_permanent_memory():
    """永続記憶のバックアップ"""
    permanent_path = Path("ai_memory/storage/permanent")
    if permanent_path.exists():
        backup_path = f"ai_memory/storage/permanent_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copytree(permanent_path, backup_path)
        print(f"✅ 永続記憶バックアップ: {backup_path}")
        return backup_path
    else:
        print("⚠️ 永続記憶ディレクトリが存在しません")
        return None

def update_core_knowledge():
    """core_knowledge.jsonにシステムマップ情報を追加"""
    permanent_path = Path("ai_memory/storage/permanent")
    core_knowledge_file = permanent_path / "core_knowledge.json"
    
    # 既存のcore_knowledge読み込み
    if core_knowledge_file.exists():
        with open(core_knowledge_file, 'r', encoding='utf-8') as f:
            core_knowledge = json.load(f)
    else:
        core_knowledge = {
            "project_type": "ソーラー蓄電システム監視",
            "critical_rules": [],
            "system_architecture": {}
        }
    
    # システムマップ情報追加
    system_map_info = {
        "last_updated": datetime.now().isoformat(),
        "system_scale": {
            "python_files": 151,
            "shell_scripts": 26, 
            "config_files": 36,
            "complexity_level": "高"
        },
        "core_modules": {
            "collector_capsule.py": "データ収集統合管理 (124行, 5関数)",
            "lvyuan_collector.py": "バッテリー監視システム (218行, 8関数)",
            "email_capsule.py": "メール機能 (72行, 1関数)",
            "weather_forecast.py": "天気予報 (139行, 2関数)",
            "hcqas_capsule.py": "AI提案システム (38行, 1関数)",
            "main.py": "システム司令塔 (66行, 1関数)"
        },
        "automation_status": {
            "active_cron_jobs": 4,
            "automation_level": "高",
            "maintenance_status": "良好"
        },
        "map_files": {
            "summary": "system_summary_*.md",
            "detailed_data": "system_map_light_*.json",
            "usage": "cat system_summary_*.md で即座システム理解"
        },
        "established_solutions": {
            "automation_control": "39個自動化スクリプト制御完了",
            "diagnostic_protocol": "バックアップ前提一時診断スクリプト手法確立",
            "system_mapping": "軽量版自動マッピングシステム構築"
        }
    }
    
    # core_knowledgeに統合
    core_knowledge["system_architecture"] = system_map_info
    
    # critical_rulesに重要項目追加
    new_rules = [
        "システム全体把握: cat system_summary_*.md で構造確認必須",
        "定期マップ更新: python3 lightweight_system_mapper.py 月1回実行",
        "新規参加者対応: システムマップ要約で迅速理解支援"
    ]
    
    for rule in new_rules:
        if rule not in core_knowledge.get("critical_rules", []):
            core_knowledge.setdefault("critical_rules", []).append(rule)
    
    # ファイル更新
    os.makedirs(permanent_path, exist_ok=True)
    with open(core_knowledge_file, 'w', encoding='utf-8') as f:
        json.dump(core_knowledge, f, indent=2, ensure_ascii=False)
    
    print(f"✅ core_knowledge.json更新完了")
    return True

def update_startup_memory():
    """ai_startup_memory.pyにシステムマップ継承を追加"""
    startup_file = "ai_memory/ai_startup_memory.py"
    
    # バックアップ
    backup_file = f"{startup_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(startup_file, backup_file)
    
    # ファイル読み込み
    with open(startup_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # システムマップ継承コード追加
    system_map_code = '''
        # システム全体マップ記憶継承
        system_map_info = core_knowledge.get('system_architecture', {})
        if system_map_info:
            print("✅ システム全体マップ記憶復旧成功")
            print(f"   📊 システム規模: Python{system_map_info.get('system_scale', {}).get('python_files', 0)}個")
            print(f"   🔧 主要モジュール: {len(system_map_info.get('core_modules', {}))}個")
            print(f"   ⚙️ 自動化レベル: {system_map_info.get('automation_status', {}).get('automation_level', '不明')}")
            print(f"   📋 確認方法: cat system_summary_*.md")
'''
    
    # core_knowledge処理の後に追加
    if "core_knowledge" in content and "system_map_info" not in content:
        # core_knowledge関連処理を探して後に追加
        lines = content.splitlines()
        insertion_point = None
        
        for i, line in enumerate(lines):
            if "core_knowledge" in line and "len(core_knowledge" in line:
                insertion_point = i + 1
                break
        
        if insertion_point:
            new_lines = []
            new_lines.extend(lines[:insertion_point])
            new_lines.extend(system_map_code.splitlines())
            new_lines.extend(lines[insertion_point:])
            
            # ファイル更新
            with open(startup_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            print(f"✅ ai_startup_memory.py更新完了")
            return True
    
    print("⚠️ ai_startup_memory.py更新をスキップ（既に存在または挿入ポイント未発見）")
    return False

def verify_integration():
    """統合結果の検証"""
    verification_items = []
    
    # core_knowledge確認
    core_knowledge_file = Path("ai_memory/storage/permanent/core_knowledge.json")
    if core_knowledge_file.exists():
        with open(core_knowledge_file, 'r', encoding='utf-8') as f:
            core_knowledge = json.load(f)
        
        if "system_architecture" in core_knowledge:
            verification_items.append("core_knowledge.json: システム構造情報追加")
        
        if any("システム全体把握" in rule for rule in core_knowledge.get("critical_rules", [])):
            verification_items.append("core_knowledge.json: 重要ルール追加")
    
    # startup_memory確認
    startup_file = Path("ai_memory/ai_startup_memory.py")
    if startup_file.exists():
        with open(startup_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "system_map_info" in content:
            verification_items.append("ai_startup_memory.py: システムマップ継承追加")
    
    return verification_items

def main():
    print("🧠 Kioku永続記憶統合スクリプト")
    print(f"実行時刻: {datetime.now()}")
    print("目的: システムマップを固定記憶領域に統合")
    
    print_section("Phase 1: 永続記憶バックアップ")
    backup_path = backup_permanent_memory()
    
    print_section("Phase 2: core_knowledge.json更新")
    core_success = update_core_knowledge()
    
    print_section("Phase 3: ai_startup_memory.py更新")
    startup_success = update_startup_memory()
    
    print_section("Phase 4: 統合検証")
    verification_items = verify_integration()
    
    print_section("🎯 永続記憶統合結果")
    
    if verification_items:
        print("🎉 kioku固定記憶統合成功！")
        for item in verification_items:
            print(f"✅ {item}")
        
        print(f"\n📋 次回AI起動時の継承内容:")
        print("   - システム全体構造が固定記憶として継承")
        print("   - 主要6モジュールの役割自動表示") 
        print("   - システムマップ確認方法の案内")
        print("   - 定期更新ルールの適用")
        
        print(f"\n🔄 次のステップ:")
        print("1. git add ai_memory/")
        print("2. git commit -m 'feat: システムマップ固定記憶統合'")
        print("3. git push")
        print("4. rm kioku_permanent_integration.py")
        
        print(f"\n🧠 恒久化完了:")
        print("   次回AIは自動的にシステム全体構造を把握します")
        
    else:
        print("❌ 統合に問題が発生しました")
        if backup_path:
            print(f"🔄 復旧: cp -r {backup_path}/* ai_memory/storage/permanent/")

if __name__ == "__main__":
    main()
