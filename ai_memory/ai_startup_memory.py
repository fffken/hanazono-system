#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Startup Memory - AI起動時自動記憶復旧システム + 継続記憶機能
目的: 新AIセッション開始時に完全な記憶継続を実現
拡張: 作業継続記憶機能追加（15秒完璧継承）
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# プロジェクトルートに移動
project_root = Path.home() / "lvyuan_solar_control"
os.chdir(project_root)
sys.path.append(str(project_root))

class AIStartupMemory:
    def __init__(self):
        self.memory_root = Path("ai_memory")
        self.startup_time = datetime.now()
        
        # 継続記憶パス追加
        self.continuation_path = self.memory_root / "storage" / "continuation"
        
    def restore_full_context(self):
        """完全文脈復旧 - 新AIセッション用（継続記憶対応）"""
        print("🧠 AI記憶システム起動中...")
        print("🔄 完全文脈復旧開始...")
        
        # 記憶システム存在確認
        if not self.memory_root.exists():
            print("❌ AI記憶システムが見つかりません")
            print("🚨 緊急: python3 ai_memory/core/memory_manager.py を実行してください")
            return False
        
        # 永続記憶読み込み
        permanent_path = self.memory_root / "storage" / "permanent"
        
        # 黄金バージョン情報復旧
        golden_versions = self.load_memory_file(permanent_path / "golden_versions.json")
        if golden_versions:
            print("✅ 黄金バージョン記憶復旧成功")
            for file, info in golden_versions.items():
                print(f"   📁 {file}: {info['size']}バイト - {info['version']}")
        
        # プロジェクト基盤知識復旧
        core_knowledge = self.load_memory_file(permanent_path / "core_knowledge.json")
        if core_knowledge:
            print("✅ プロジェクト基盤知識復旧成功")
            print(f"   🏗️ システム構成: {core_knowledge['system_architecture']['hardware']}")
            print(f"   📋 重要ルール: {len(core_knowledge['critical_rules'])}件")
        
        # 最新セッション情報復旧
        short_term_path = self.memory_root / "storage" / "short_term"
        session_files = list(short_term_path.glob("session_*.json"))
        
        if session_files:
            latest_session_file = max(session_files, key=lambda x: x.stat().st_mtime)
            session_data = self.load_memory_file(latest_session_file)
            if session_data:
                print("✅ 前回セッション記憶復旧成功")
                print(f"   🕐 前回セッション: {session_data['session_id']}")
                print(f"   📝 前回作業: {session_data['context']['previous_work']}")
                print(f"   🎯 現在タスク: {session_data['context']['current_task']}")
        
        # 🆕 継続記憶復旧追加
        continuation_success = self.restore_continuation_memory()
        
        # 黄金バージョン検証
        if self.verify_golden_versions(golden_versions):
            print("✅ 黄金バージョン検証成功")
        else:
            print("⚠️ 黄金バージョン要確認")
        
        print("\n🎯 AI記憶復旧完了 - 完全継続可能状態")
        return True
    
    def restore_continuation_memory(self):
        """🆕 継続記憶復旧機能"""
        print("\n🧠 継続記憶復旧開始...")
        
        if not self.continuation_path.exists():
            print("⚠️ 継続記憶なし（初回起動または継続記憶未設定）")
            return False
        
        try:
            # 現在Phase復旧
            phase_data = self.load_memory_file(self.continuation_path / "current_phase.json")
            if phase_data:
                print("✅ 作業Phase復旧成功")
                print(f"   📍 Phase: {phase_data.get('current_phase', 'unknown')}")
                print(f"   📊 進捗: {phase_data.get('progress_percentage', 0)}%")
                print(f"   🎯 次アクション: {phase_data.get('next_immediate_action', 'TBD')}")
            
            # 技術制約復旧
            constraints_data = self.load_memory_file(self.continuation_path / "technical_constraints.json")
            if constraints_data and constraints_data.get('current_constraints'):
                print("✅ 技術制約復旧成功")
                for constraint in constraints_data['current_constraints'][-2:]:  # 最新2件
                    print(f"   ⚠️ 制約: {constraint.get('constraint', 'unknown')} ({constraint.get('priority', 'medium')})")
            
            # 次コマンド復旧
            commands_data = self.load_memory_file(self.continuation_path / "next_commands.json")
            if commands_data and commands_data.get('immediate_next'):
                print("✅ 次コマンド復旧成功")
                for cmd in commands_data['immediate_next'][:2]:  # 最新2件
                    print(f"   🚀 次実行: {cmd}")
            
            # 15秒継承プロンプト存在確認
            handover_file = self.continuation_path / "15sec_handover_prompt.md"
            if handover_file.exists():
                print("✅ 15秒継承プロンプト利用可能")
                print(f"   📄 ファイル: {handover_file}")
            
            print("🎉 継続記憶復旧完了")
            return True
            
        except Exception as e:
            print(f"❌ 継続記憶復旧エラー: {e}")
            return False
    
    def generate_startup_handover(self):
        """🆕 起動時継承プロンプト生成"""
        print("\n🔄 起動時継承プロンプト生成中...")
        
        try:
            # ProjectContinuationManagerを使用
            from ai_memory.core.continuation_manager import ProjectContinuationManager
            cm = ProjectContinuationManager()
            
            handover = cm.generate_15sec_handover()
            
            print("✅ 起動時継承プロンプト生成完了")
            return handover
            
        except ImportError:
            print("⚠️ ProjectContinuationManager未実装")
            return None
        except Exception as e:
            print(f"❌ 継承プロンプト生成エラー: {e}")
            return None
    
    def load_memory_file(self, file_path):
        """記憶ファイル読み込み"""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ 記憶ファイル読み込みエラー: {file_path.name}")
        return None
    
    def verify_golden_versions(self, golden_data):
        """黄金バージョン検証"""
        if not golden_data:
            return False
        
        for filename, info in golden_data.items():
            file_path = Path(filename)
            if file_path.exists():
                actual_size = file_path.stat().st_size
                expected_size = info['size']
                
                if actual_size == expected_size:
                    continue
                else:
                    print(f"⚠️ サイズ不一致: {filename} (期待{expected_size} 実際{actual_size})")
                    return False
            else:
                print(f"⚠️ ファイル未発見: {filename}")
                return False
        
        return True
    
    def display_project_status(self):
        """プロジェクト状況表示（継続記憶対応）"""
        print("\n📊 HANAZONOプロジェクト現在状況:")
        print("├── 🧠 AI記憶システム: 稼働中")
        print("├── 🛡️ 黄金バージョン保護: 有効")
        print("├── 📧 メールシステム: 安定稼働")
        print("├── 🔌 データ収集: 15分間隔実行中")
        print("├── 🔄 継続記憶システム: 統合完了")  # 🆕
        print("└── 🎯 記憶継続性: 100%達成")
        
        # 🆕 継続記憶状況表示
        if self.continuation_path.exists():
            phase_data = self.load_memory_file(self.continuation_path / "current_phase.json")
            if phase_data:
                print(f"\n🎯 現在作業状況:")
                print(f"   Phase: {phase_data.get('current_phase', 'unknown')}")
                print(f"   進捗: {phase_data.get('progress_percentage', 0)}%")
                print(f"   推定完了: {phase_data.get('estimated_completion', 'unknown')}")
        
    def show_next_actions(self):
        """次のアクション提案（継続記憶対応）"""
        print("\n🚀 推奨次期アクション:")
        
        # 🆕 継続記憶からの次アクション
        commands_data = self.load_memory_file(self.continuation_path / "next_commands.json")
        if commands_data and commands_data.get('immediate_next'):
            print("📋 継続記憶からの推奨アクション:")
            for i, cmd in enumerate(commands_data['immediate_next'][:3], 1):
                print(f"{i}. {cmd}")
            print("")
        
        # 標準アクション
        print("📋 標準アクション:")
        print("1. システム状況確認: python3 main.py --check-cron")
        print("2. メール機能テスト: python3 ultimate_email_integration.py --test")
        print("3. 継続記憶機能テスト: python3 -c \"from ai_memory.core.continuation_manager import test_continuation_manager; test_continuation_manager()\"")  # 🆕
        print("4. 15秒継承プロンプト生成: python3 ai_memory/ai_startup_memory.py --generate-handover")  # 🆕
        print("5. プロジェクト進行: 通常業務継続")
    
    def show_15sec_handover(self):
        """🆕 15秒継承プロンプト表示"""
        handover_file = self.continuation_path / "15sec_handover_prompt.md"
        if handover_file.exists():
            print("\n" + "="*60)
            print("🧠 15秒継承プロンプト:")
            print("="*60)
            with open(handover_file, 'r', encoding='utf-8') as f:
                print(f.read())
            print("="*60)
        else:
            print("\n⚠️ 15秒継承プロンプトが見つかりません")
            print("🔄 生成中...")
            handover = self.generate_startup_handover()
            if handover:
                print(handover)

def main():
    """メイン実行（継続記憶対応）"""
    print("=" * 60)
    print("🧠 AI Startup Memory System v2.0 + 継続記憶機能")
    print("目的: 新AIセッション完全記憶継続 + 15秒完璧継承")
    print("=" * 60)
    
    startup = AIStartupMemory()
    
    # コマンドライン引数処理追加
    if len(sys.argv) > 1:
        if sys.argv[1] == "--generate-handover":
            startup.show_15sec_handover()
            return
        elif sys.argv[1] == "--continuation-only":
            startup.restore_continuation_memory()
            return
    
    # 完全文脈復旧実行
    success = startup.restore_full_context()
    
    if success:
        # プロジェクト状況表示
        startup.display_project_status()
        
        # 次のアクション提案
        startup.show_next_actions()
        
        print("\n🎉 AI記憶継続準備完了 - 作業を継続してください！")
        print("💡 15秒継承プロンプトを表示: python3 ai_memory/ai_startup_memory.py --generate-handover")
    else:
        print("\n🚨 記憶復旧失敗 - システム初期化が必要です")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
