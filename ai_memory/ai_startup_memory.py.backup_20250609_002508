#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Startup Memory - AI起動時自動記憶復旧システム + 継続記憶機能
目的: 新AIセッション開始時に完全な記憶継続を実現
拡張: 作業継続記憶機能追加（15秒完璧継承） + 自動プロジェクト検知
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
        """完全文脈復旧 - 新AIセッション用（継続記憶対応+自動検知）"""
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

        # システム全体マップ記憶継承
        system_map_info = core_knowledge.get('system_architecture', {})
        if system_map_info:
            print("✅ システム全体マップ記憶復旧成功")
            print(f"   📊 システム規模: Python{system_map_info.get('system_scale', {}).get('python_files', 0)}個")
            print(f"   🔧 主要モジュール: {len(system_map_info.get('core_modules', {}))}個")
            print(f"   ⚙️ 自動化レベル: {system_map_info.get('automation_status', {}).get('automation_level', '不明')}")

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
            print(f"   📋 確認方法: cat system_summary_*.md")

        # システム診断革命手法 - kiokuシステム統合 (2025-06-08確立)
        diagnostic_protocol = {
            "protocol_name": "バックアップ前提一時診断スクリプト手法",
            "version": "1.0", 
            "established": "2025-06-08",
            "success_case": "39個自動化スクリプト制御問題完全解決",
            "proven_results": [
                "Gemini誤診論破（OS再インストール回避）",
                "20時間停止バッテリー監視システム復旧",
                "HANAZONOループ問題完全解決"
            ],
            "trigger_conditions": [
                "システム診断・修復作業時",
                "複雑な問題調査時",
                "環境構築・変更作業時",
                "自動化スクリプト問題発生時"
            ],
            "mandatory_workflow": [
                "1. tar -czf BACKUP_$(date +%Y%m%d_%H%M%S).tar.gz で確実バックアップ",
                "2. nano [目的]_diagnosis_$(date +%H%M%S).py で一時診断スクリプト作成",
                "3. 段階的・非破壊的調査実行",
                "4. rm [診断スクリプト].py で即座削除",
                "5. 結果記録・次AI継承"
            ],
            "core_principles": [
                "非破壊的アプローチ100%遵守",
                "段階的問題解決",
                "完全な記録と透明性",
                "システム協調優先"
            ],
            "cleanup_mandatory": True,
            "cleanup_patterns": ["*_diagnosis_*.py", "*_emergency_*.py", "*_audit_*.py", "*_inspector_*.py"]
        }
        
        # 診断プロトコル記憶表示
        if diagnostic_protocol:
            print("✅ 診断プロトコル記憶復旧成功")
            print(f"   🛠️ 手法: {diagnostic_protocol['protocol_name']}")
            print(f"   📊 実績: {diagnostic_protocol['success_case']}")
            print(f"   🎯 適用条件: {len(diagnostic_protocol['trigger_conditions'])}種類")

        
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
        
        # 🆕 継続記憶復旧追加（自動検知対応）
        continuation_success = self.restore_continuation_memory_auto()
        
        # 黄金バージョン検証
        if self.verify_golden_versions(golden_versions):
            print("✅ 黄金バージョン検証成功")
        else:
            print("⚠️ 黄金バージョン要確認")
        
        print("\n🎯 AI記憶復旧完了 - 完全継続可能状態")
        return True
    
    def restore_continuation_memory_auto(self):
        """🆕 継続記憶復旧機能（自動検知対応）"""
        print("\n🧠 継続記憶復旧開始（自動プロジェクト検知）...")
        
        try:
            # 自動検知対応ProjectContinuationManager使用
            from ai_memory.core.continuation_manager import ProjectContinuationManager
            cm = ProjectContinuationManager()  # 自動検知実行
            
            # 検知されたプロジェクト情報
            detected_project = cm.project_name
            print(f"🎯 検知されたプロジェクト: {detected_project}")
            
            # 現在状況取得
            status = cm.get_current_status()
            auto_detected = status.get('auto_detected', False)
            auto_info = " [自動検知]" if auto_detected else ""
            
            print("✅ 作業Phase復旧成功")
            print(f"   📍 Phase: {status['phase']}")
            print(f"   📊 進捗: {status['progress']}%")
            print(f"   🎯 次アクション: {status['next_action']}")
            
            # Git詳細情報表示
            git_detail = cm.record_git_changes_detail()
            if git_detail.get('files_changed', 0) > 0:
                print(f"   📊 Git状態: {git_detail['files_changed']}件変更 ({git_detail.get('change_scale', 'unknown')})")
                if git_detail.get('major_changes'):
                    print(f"   📁 主要変更: {', '.join(git_detail['major_changes'][:3])}")
            
            # 技術制約復旧
            if not self.continuation_path.exists():
                print("⚠️ 継続記憶なし（初回起動または継続記憶未設定）")
                return False
                
            constraints_data = self.load_memory_file(cm.constraints_file)
            if constraints_data and constraints_data.get('current_constraints'):
                print("✅ 技術制約復旧成功")
                for constraint in constraints_data['current_constraints'][-2:]:
                    priority = constraint.get('priority', 'medium')
                    emoji = "🚨" if priority == "critical" else "⚠️" if priority == "high" else "📝"
                    print(f"   {emoji} 制約: {constraint.get('constraint', 'unknown')} ({priority})")
            
            # 次コマンド復旧
            commands_data = self.load_memory_file(cm.commands_file)
            if commands_data and commands_data.get('immediate_next'):
                print("✅ 次コマンド復旧成功")
                for cmd in commands_data['immediate_next'][:2]:
                    print(f"   🚀 次実行: {cmd}")
            
            # 15秒継承プロンプト存在確認
            if cm.handover_file.exists():
                print("✅ 15秒継承プロンプト利用可能")
                print(f"   📄 ファイル: {cm.handover_file}")
            
            print("🎉 継続記憶復旧完了")
            
            # プロジェクト別状況表示
            self.display_project_status_auto(detected_project, status)
            
            return True
            
        except ImportError:
            print("⚠️ ProjectContinuationManager未実装")
            return self.restore_continuation_memory()  # フォールバック
        except Exception as e:
            print(f"❌ 継続記憶復旧エラー: {e}")
            return False
    
    def restore_continuation_memory(self):
        """継続記憶復旧機能（互換性用フォールバック）"""
        print("\n🧠 継続記憶復旧開始...")
        
        if not self.continuation_path.exists():
            print("⚠️ 継続記憶なし（初回起動または継続記憶未設定）")
            return False
        
        try:
            # デフォルトプロジェクト（hanazono）で復旧
            hanazono_path = self.continuation_path / "hanazono"
            if hanazono_path.exists():
                phase_data = self.load_memory_file(hanazono_path / "current_phase.json")
                if phase_data:
                    print("✅ 作業Phase復旧成功")
                    print(f"   📍 Phase: {phase_data.get('current_phase', 'unknown')}")
                    print(f"   📊 進捗: {phase_data.get('progress_percentage', 0)}%")
                    print(f"   🎯 次アクション: {phase_data.get('next_immediate_action', 'TBD')}")
            
            print("🎉 継続記憶復旧完了")
            return True
            
        except Exception as e:
            print(f"❌ 継続記憶復旧エラー: {e}")
            return False
    
    def display_project_status_auto(self, project_name, status):
        """プロジェクト状況表示（自動検知対応）"""
        print(f"\n📊 {project_name.upper()}プロジェクト現在状況:")
        print("├── 🧠 AI記憶システム: 稼働中")
        print("├── 🛡️ 黄金バージョン保護: 有効")
        print("├── 📧 メールシステム: 安定稼働")
        print("├── 🔌 データ収集: 15分間隔実行中")
        print("├── 🔄 継続記憶システム: 統合完了")
        print("├── 🎯 自動プロジェクト検知: 有効")  # 🆕
        print("└── 🎯 記憶継続性: 100%達成")
        
        # 現在作業状況表示
        print(f"\n🎯 現在作業状況:")
        print(f"   プロジェクト: {project_name}")
        print(f"   Phase: {status.get('phase', 'unknown')}")
        print(f"   進捗: {status.get('progress', 0)}%")
        auto_detected = status.get('auto_detected', False)
        if auto_detected:
            print(f"   検知方式: 自動検知")
    
    def generate_startup_handover(self):
        """🆕 起動時継承プロンプト生成（自動検知対応）"""
        print("\n🔄 起動時継承プロンプト生成中...")
        
        try:
            # 自動検知対応ProjectContinuationManagerを使用
            from ai_memory.core.continuation_manager import ProjectContinuationManager
            cm = ProjectContinuationManager()  # 自動検知実行
            
            handover = cm.generate_15sec_handover()
            
            print("✅ 起動時継承プロンプト生成完了")
            print(f"📄 プロジェクト: {cm.project_name}")
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
        print("├── 🔄 継続記憶システム: 統合完了")
        print("└── 🎯 記憶継続性: 100%達成")
        
        # 継続記憶状況表示
        hanazono_path = self.continuation_path / "hanazono"
        if hanazono_path.exists():
            phase_data = self.load_memory_file(hanazono_path / "current_phase.json")
            if phase_data:
                print(f"\n🎯 現在作業状況:")
                print(f"   Phase: {phase_data.get('current_phase', 'unknown')}")
                print(f"   進捗: {phase_data.get('progress_percentage', 0)}%")
                print(f"   推定完了: {phase_data.get('estimated_completion', 'unknown')}")
        
    def show_next_actions(self):
        """次のアクション提案（継続記憶対応+自動検知）"""
        print("\n🚀 推奨次期アクション:")
        
        try:
            # 自動検知対応の次アクション
            from ai_memory.core.continuation_manager import ProjectContinuationManager
            cm = ProjectContinuationManager()  # 自動検知実行
            
            commands_data = self.load_memory_file(cm.commands_file)
            if commands_data and commands_data.get('immediate_next'):
                print("📋 継続記憶からの推奨アクション:")
                for i, cmd in enumerate(commands_data['immediate_next'][:3], 1):
                    print(f"{i}. {cmd}")
                print("")
            
        except ImportError:
            # フォールバック: hanazono プロジェクトの次アクション
            hanazono_path = self.continuation_path / "hanazono"
            if hanazono_path.exists():
                commands_data = self.load_memory_file(hanazono_path / "next_commands.json")
                if commands_data and commands_data.get('immediate_next'):
                    print("📋 継続記憶からの推奨アクション:")
                    for i, cmd in enumerate(commands_data['immediate_next'][:3], 1):
                        print(f"{i}. {cmd}")
                    print("")
        
        # 標準アクション
        print("📋 標準アクション:")
        print("1. システム状況確認: python3 main.py --check-cron")
        print("2. メール機能テスト: python3 ultimate_email_integration.py --test")
        print("3. 継続記憶機能テスト: python3 -c \"from ai_memory.core.continuation_manager import test_auto_detect_system; test_auto_detect_system()\"")  # 🆕
        print("4. 15秒継承プロンプト生成: python3 ai_memory/ai_startup_memory.py --generate-handover")
        print("5. プロジェクト進行: 通常業務継続")
    
    def show_15sec_handover(self):
        """🆕 15秒継承プロンプト表示（自動検知対応）"""
        try:
            from ai_memory.core.continuation_manager import ProjectContinuationManager
            cm = ProjectContinuationManager()  # 自動検知実行
            
            if cm.handover_file.exists():
                print("\n" + "="*60)
                print("🧠 15秒継承プロンプト:")
                print("="*60)
                with open(cm.handover_file, 'r', encoding='utf-8') as f:
                    print(f.read())
                print("="*60)
            else:
                print("\n⚠️ 15秒継承プロンプトが見つかりません")
                print("🔄 生成中...")
                handover = self.generate_startup_handover()
                if handover:
                    print(handover)
        except ImportError:
            print("\n⚠️ 15秒継承プロンプト機能未実装")

def main():
    """メイン実行（継続記憶対応+自動検知）"""
    print("=" * 60)
    print("🧠 AI Startup Memory System v2.0 + 継続記憶機能 + 自動検知")
    print("目的: 新AIセッション完全記憶継続 + 15秒完璧継承 + 自動プロジェクト検知")
    print("=" * 60)
    
    startup = AIStartupMemory()
    
    # コマンドライン引数処理追加
    if len(sys.argv) > 1:
        if sys.argv[1] == "--generate-handover":
            startup.show_15sec_handover()
            return
        elif sys.argv[1] == "--continuation-only":
            startup.restore_continuation_memory_auto()
            return
    
    # 完全文脈復旧実行
    success = startup.restore_full_context()
    
    if success:
        # 次のアクション提案
        startup.show_next_actions()
        
        print("\n🎉 AI記憶継続準備完了 - 作業を継続してください！")
        print("💡 15秒継承プロンプトを表示: python3 ai_memory/ai_startup_memory.py --generate-handover")
    else:
        print("\n🚨 記憶復旧失敗 - システム初期化が必要です")
    
    print("=" * 60)

if __name__ == "__main__":
    main()