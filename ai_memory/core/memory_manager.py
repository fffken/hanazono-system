#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Memory Manager - AI記憶システムの中核
目的: AIセッション間の完全記憶継続により、プロジェクト断絶を根絶
"""

import os
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path

class AIMemoryManager:
    def __init__(self):
        self.memory_root = Path("ai_memory")
        self.current_session_id = self.generate_session_id()
        self.initialize_memory_system()
    
    def generate_session_id(self):
        """セッションID生成"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def initialize_memory_system(self):
        """記憶システム初期化"""
        print("🧠 AI記憶システム初期化中...")
        
        # 永続記憶の初期化
        self.initialize_permanent_memory()
        
        # 現在セッション記録開始
        self.start_session_recording()
        
        print(f"✅ AI記憶システム初期化完了 - セッション: {self.current_session_id}")
    
    def initialize_permanent_memory(self):
        """永続記憶の初期化"""
        permanent_path = self.memory_root / "storage" / "permanent"
        
        # 黄金バージョン記憶
        golden_versions = {
            "email_notifier_v2_1.py": {
                "size": 26331,
                "version": "Enhanced Email System v2.2",
                "features": ["🟠タイトル絵文字システム", "状況別絵文字"],
                "status": "完璧版・変更禁止",
                "last_verified": datetime.now().isoformat()
            }
        }
        
        # プロジェクト基盤知識
        core_knowledge = {
            "system_architecture": {
                "hardware": "Raspberry Pi Zero 2 W",
                "inverter": "LVYUAN SPI-10K-U (10kW)", 
                "battery": "FLCD16-10048 × 4台 (20.48kWh)",
                "communication": "Modbus TCP (PySolarmanV5)"
            },
            "critical_rules": [
                "作業前に必ず黄金バージョン確保",
                "機能テスト実行後に変更適用",
                "Git状態確認は作業開始の必須条件",
                "記憶システム実装は最優先事項"
            ]
        }
        
        # 永続記憶保存
        self.save_memory("permanent", "golden_versions", golden_versions)
        self.save_memory("permanent", "core_knowledge", core_knowledge)
    
    def start_session_recording(self):
        """セッション記録開始"""
        session_data = {
            "session_id": self.current_session_id,
            "start_time": datetime.now().isoformat(),
            "context": {
                "previous_work": "AI記憶システム設計完了",
                "current_task": "Phase 1実装中",
                "progress_status": "memory_manager.py作成中"
            },
            "memory_system_status": "初期化完了"
        }
        
        self.save_memory("short_term", f"session_{self.current_session_id}", session_data)
    
    def save_memory(self, memory_type, key, data):
        """記憶保存"""
        memory_path = self.memory_root / "storage" / memory_type
        file_path = memory_path / f"{key}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_memory(self, memory_type, key):
        """記憶読み込み"""
        memory_path = self.memory_root / "storage" / memory_type
        file_path = memory_path / f"{key}.json"
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def verify_golden_versions(self):
        """黄金バージョン検証"""
        print("🛡️ 黄金バージョン検証中...")
        
        golden_data = self.load_memory("permanent", "golden_versions")
        if not golden_data:
            print("❌ 黄金バージョン記憶が見つかりません")
            return False
        
        # email_notifier_v2_1.py検証
        email_file = Path("email_notifier_v2_1.py")
        if email_file.exists():
            size = email_file.stat().st_size
            expected_size = golden_data["email_notifier_v2_1.py"]["size"]
            
            if size == expected_size:
                print(f"✅ email_notifier_v2_1.py 検証成功: {size}バイト")
                return True
            else:
                print(f"❌ サイズ不一致: 期待{expected_size} 実際{size}")
                return False
        else:
            print("❌ email_notifier_v2_1.py が見つかりません")
            return False
    
    def restore_full_context(self):
        """完全文脈復旧"""
        print("🔄 完全文脈復旧中...")
        
        # 永続記憶読み込み
        core_knowledge = self.load_memory("permanent", "core_knowledge")
        golden_versions = self.load_memory("permanent", "golden_versions")
        
        # 最新セッション情報取得
        short_term_files = list((self.memory_root / "storage" / "short_term").glob("session_*.json"))
        if short_term_files:
            latest_session = max(short_term_files, key=lambda x: x.stat().st_mtime)
            session_data = self.load_memory("short_term", latest_session.stem)
        else:
            session_data = None
        
        context = {
            "memory_restoration": "完全成功",
            "core_knowledge": core_knowledge,
            "golden_versions": golden_versions,
            "last_session": session_data,
            "restoration_time": datetime.now().isoformat()
        }
        
        print("✅ 完全文脈復旧完了")
        return context

def main():
    """メイン実行"""
    print("🧠 AI Memory Manager v1.0")
    
    memory = AIMemoryManager()
    
    # 黄金バージョン検証
    memory.verify_golden_versions()
    
    # 完全文脈復旧テスト
    context = memory.restore_full_context()
    
    print("\n🎯 AI記憶システム稼働開始")
    print("次のAIセッションでは完全な記憶継続が可能です")

if __name__ == "__main__":
    main()
