"""
🧠 kioku System - ProjectContinuationManager
Purpose: 15秒完璧継承できる作業継続記憶機能
Created: 2025-06-04
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
import subprocess

class ProjectContinuationManager:
    """作業継続記憶管理クラス - 15秒完璧継承システム"""
    
    def __init__(self):
        self.base_path = Path("ai_memory/storage/continuation")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # 継続記憶ファイルパス
        self.phase_file = self.base_path / "current_phase.json"
        self.constraints_file = self.base_path / "technical_constraints.json"
        self.commands_file = self.base_path / "next_commands.json" 
        self.patterns_file = self.base_path / "success_patterns.json"
        self.handover_file = self.base_path / "15sec_handover_prompt.md"
        
        # 初期化
        self._initialize_files()
    
    def _initialize_files(self):
        """継続記憶ファイル初期化"""
        
        # current_phase.json初期化
        if not self.phase_file.exists():
            initial_phase = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "current_phase": "system_initialization",
                "phase_number": 1,
                "step": "setup",
                "progress_percentage": 0,
                "estimated_completion": "30_minutes",
                "description": "kiokuシステム継続記憶機能初期化",
                "next_immediate_action": "ProjectContinuationManager実装"
            }
            self._save_json(self.phase_file, initial_phase)
        
        # technical_constraints.json初期化
        if not self.constraints_file.exists():
            initial_constraints = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "resolved_issues": [],
                "current_constraints": [],
                "technical_decisions": []
            }
            self._save_json(self.constraints_file, initial_constraints)
        
        # next_commands.json初期化
        if not self.commands_file.exists():
            initial_commands = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "immediate_next": ["python3 -c \"from ai_memory.core.continuation_manager import ProjectContinuationManager; cm=ProjectContinuationManager(); print('✅ 継続記憶システム初期化完了')\""],
                "phase_completion": [],
                "rollback_commands": []
            }
            self._save_json(self.commands_file, initial_commands)
        
        # success_patterns.json初期化
        if not self.patterns_file.exists():
            initial_patterns = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "successful_patterns": [],
                "failure_patterns": [],
                "best_practices": [
                    "実装前必ずバックアップ",
                    "段階的テスト実行",
                    "非破壊的作業徹底"
                ]
            }
            self._save_json(self.patterns_file, initial_patterns)
    
    def save_work_snapshot(self, phase, step, progress, description, next_action):
        """作業スナップショット保存"""
        snapshot = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "current_phase": phase,
            "phase_number": self._extract_phase_number(phase),
            "step": step,
            "progress_percentage": progress,
            "estimated_completion": self._estimate_completion(progress),
            "description": description,
            "next_immediate_action": next_action,
            "git_status": self._get_git_status(),
            "active_files": self._get_active_files()
        }
        
        self._save_json(self.phase_file, snapshot)
        print(f"📸 作業スナップショット保存: {phase} - {step} ({progress}%)")
        return True
    
    def generate_15sec_handover(self):
        """15秒継承プロンプト生成"""
        try:
            # 各ファイルからデータ読み込み
            phase_data = self._load_json(self.phase_file)
            constraints_data = self._load_json(self.constraints_file)
            commands_data = self._load_json(self.commands_file)
            patterns_data = self._load_json(self.patterns_file)
            
            # Git状態取得
            git_status = self._get_git_status()
            
            # 15秒継承プロンプト生成
            handover = f"""🧠 **15秒完璧継承プロンプト** - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## ⚡ 即座実行情報
```bash
cd ~/lvyuan_solar_control
# 現在Phase: {phase_data.get('current_phase', 'unknown')}
# Progress: {phase_data.get('progress_percentage', 0)}%
# Git状態: {git_status}
```

## 🎯 現在状況
- **Phase**: {phase_data.get('current_phase', 'unknown')} (Step: {phase_data.get('step', 'unknown')})
- **進捗**: {phase_data.get('progress_percentage', 0)}% 完了
- **説明**: {phase_data.get('description', 'No description')}
- **次アクション**: {phase_data.get('next_immediate_action', 'TBD')}

## 🚨 重要制約
{self._format_constraints(constraints_data)}

## 🚀 次のアクション
```bash
{self._format_next_commands(commands_data)}
```

## 💡 成功パターン適用
{self._format_success_patterns(patterns_data)}

## 🔧 即座実行コマンド
```bash
{commands_data.get('immediate_next', ['# No immediate commands'])[0] if commands_data.get('immediate_next') else '# No commands available'}
```

## 📊 技術状況
- **Git状態**: {git_status}
- **アクティブファイル**: {', '.join(self._get_active_files()[:3])}
- **推定完了**: {phase_data.get('estimated_completion', 'unknown')}

**この継承で即座に作業継続可能！**
"""
            
            # 継承プロンプトファイル保存
            with open(self.handover_file, 'w', encoding='utf-8') as f:
                f.write(handover)
            
            print("✅ 15秒継承プロンプト生成完了")
            print(f"📄 保存先: {self.handover_file}")
            return handover
            
        except Exception as e:
            print(f"❌ 継承プロンプト生成エラー: {e}")
            return "🚨 継承プロンプト生成失敗"
    
    def record_technical_constraint(self, constraint, impact, priority="medium"):
        """技術制約記録"""
        try:
            constraints_data = self._load_json(self.constraints_file)
            
            new_constraint = {
                "constraint": constraint,
                "impact": impact,
                "priority": priority,
                "recorded_at": datetime.now(timezone.utc).isoformat()
            }
            
            if "current_constraints" not in constraints_data:
                constraints_data["current_constraints"] = []
            
            constraints_data["current_constraints"].append(new_constraint)
            constraints_data["timestamp"] = datetime.now(timezone.utc).isoformat()
            
            self._save_json(self.constraints_file, constraints_data)
            print(f"📝 技術制約記録: {constraint}")
            return True
            
        except Exception as e:
            print(f"❌ 制約記録エラー: {e}")
            return False
    
    def save_next_command(self, command_type, commands):
        """次ステップコマンド保存"""
        try:
            commands_data = self._load_json(self.commands_file)
            
            commands_data[command_type] = commands if isinstance(commands, list) else [commands]
            commands_data["timestamp"] = datetime.now(timezone.utc).isoformat()
            
            self._save_json(self.commands_file, commands_data)
            print(f"💾 次ステップコマンド保存: {command_type}")
            return True
            
        except Exception as e:
            print(f"❌ コマンド保存エラー: {e}")
            return False
    
    def mark_phase_complete(self, phase, success_factors=None):
        """Phase完了マーキング"""
        try:
            patterns_data = self._load_json(self.patterns_file)
            
            completion_record = {
                "pattern": f"{phase}_completion",
                "phase": phase,
                "completion_time": datetime.now(timezone.utc).isoformat(),
                "success_factors": success_factors or ["段階的実装", "テスト完了"]
            }
            
            if "successful_patterns" not in patterns_data:
                patterns_data["successful_patterns"] = []
            
            patterns_data["successful_patterns"].append(completion_record)
            patterns_data["timestamp"] = datetime.now(timezone.utc).isoformat()
            
            self._save_json(self.patterns_file, patterns_data)
            print(f"🎉 Phase完了記録: {phase}")
            return True
            
        except Exception as e:
            print(f"❌ 完了記録エラー: {e}")
            return False
    
    def get_current_status(self):
        """現在状況取得"""
        phase_data = self._load_json(self.phase_file)
        return {
            "phase": phase_data.get('current_phase', 'unknown'),
            "step": phase_data.get('step', 'unknown'),
            "progress": phase_data.get('progress_percentage', 0),
            "next_action": phase_data.get('next_immediate_action', 'TBD')
        }
    
    # Helper methods
    def _load_json(self, file_path):
        """JSONファイル安全読み込み"""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"⚠️ JSON読み込みエラー: {file_path} - {e}")
            return {}
    
    def _save_json(self, file_path, data):
        """JSONファイル安全保存"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ JSON保存エラー: {file_path} - {e}")
            return False
    
    def _extract_phase_number(self, phase):
        """Phase番号抽出"""
        try:
            import re
            match = re.search(r'(\d+)', phase)
            return int(match.group(1)) if match else 1
        except:
            return 1
    
    def _estimate_completion(self, progress):
        """完了時間推定"""
        if progress >= 90:
            return "5_minutes"
        elif progress >= 70:
            return "15_minutes"
        elif progress >= 50:
            return "30_minutes"
        else:
            return "60_minutes"
    
    def _get_git_status(self):
        """Git状態取得"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd='.')
            lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
            return f"{len(lines)} files changed" if lines else "clean"
        except:
            return "unknown"
    
    def _get_active_files(self):
        """アクティブファイル一覧"""
        try:
            result = subprocess.run(['git', 'diff', '--name-only', 'HEAD'], 
                                  capture_output=True, text=True, cwd='.')
            files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            return [f for f in files if f][:5]  # 最大5ファイル
        except:
            return []
    
    def _format_constraints(self, constraints_data):
        """制約フォーマット"""
        constraints = constraints_data.get('current_constraints', [])
        if not constraints:
            return "- 現在制約なし"
        
        formatted = []
        for c in constraints[-3:]:  # 最新3件
            formatted.append(f"- **{c.get('constraint', 'Unknown')}**: {c.get('impact', 'No impact')} ({c.get('priority', 'medium')})")
        
        return '\n'.join(formatted)
    
    def _format_next_commands(self, commands_data):
        """次コマンドフォーマット"""
        immediate = commands_data.get('immediate_next', [])
        return '\n'.join(immediate[:3]) if immediate else "# 次のコマンドはありません"
    
    def _format_success_patterns(self, patterns_data):
        """成功パターンフォーマット"""
        patterns = patterns_data.get('successful_patterns', [])
        if not patterns:
            return "- 新規実装（成功パターン蓄積中）"
        
        latest = patterns[-1]
        return f"- **適用パターン**: {latest.get('pattern', 'Unknown')}\n- **成功要因**: {', '.join(latest.get('success_factors', []))}"


# テスト用関数
def test_continuation_manager():
    """継続記憶システムテスト"""
    print("🧪 継続記憶システムテスト開始")
    
    try:
        # インスタンス作成
        cm = ProjectContinuationManager()
        print("✅ ProjectContinuationManager初期化完了")
        
        # スナップショット保存テスト
        cm.save_work_snapshot(
            phase="kioku_system_expansion",
            step="implementation",
            progress=50,
            description="kioku継続記憶機能実装中",
            next_action="ai_startup_memory.py拡張"
        )
        
        # 制約記録テスト
        cm.record_technical_constraint(
            constraint="ラズパイターミナル行数制限",
            impact="コピペ30-40行制限",
            priority="high"
        )
        
        # 次コマンド保存テスト
        cm.save_next_command("immediate_next", [
            "python3 -c \"from ai_memory.core.continuation_manager import test_continuation_manager; test_continuation_manager()\"",
            "nano ai_memory/ai_startup_memory.py  # 拡張実装"
        ])
        
        # 15秒継承プロンプト生成テスト
        handover = cm.generate_15sec_handover()
        print("✅ 15秒継承プロンプト生成完了")
        
        # 現在状況確認
        status = cm.get_current_status()
        print(f"📊 現在状況: {status['phase']} - {status['step']} ({status['progress']}%)")
        
        print("🎉 継続記憶システムテスト完了！")
        return True
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        return False


if __name__ == "__main__":
    test_continuation_manager()
