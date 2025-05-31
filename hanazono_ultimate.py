#!/usr/bin/env python3
"""
HANAZONO 究極引き継ぎシステム v2.0
シンプル・強力・改善しやすい設計
"""

import sys
import json
import subprocess
import glob
from datetime import datetime
from pathlib import Path

class HANAZONOUltimate:
    def __init__(self):
        self.base_dir = Path.home() / "lvyuan_solar_control"
        self.config_file = self.base_dir / "handover_config.json"
        self.load_config()
    
    def load_config(self):
        """設定読み込み（カスタマイズ可能）"""
        default_config = {
            "instant_items": [
                "git_status", "system_status", "urgency_level", 
                "available_commands", "recommended_actions"
            ],
            "detail_items": [
                "technical_specs", "recent_changes", "error_logs",
                "performance_metrics", "full_documentation"
            ],
            "update_sources": [
                "AI_WORK_RULES.md", "PROJECT_STATUS.md", 
                "HANDOVER_PROMPT.md", "git_info"
            ]
        }
        
        if self.config_file.exists():
            with open(self.config_file) as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """設定保存"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def instant_handover(self):
        """瞬間把握（5秒以内）"""
        print("🏆 HANAZONOシステム - 究極モード起動")
        print("=" * 50)
        print("⚡ 瞬間把握実行中...")
        
        # 設定可能な項目を順次実行
        for item in self.config["instant_items"]:
            if hasattr(self, f"get_{item}"):
                getattr(self, f"get_{item}")()
        
        print("\n💡 詳細情報が必要な場合:")
        print("  hanazono detail   # 技術仕様・詳細分析")
        print("  hanazono update   # 引き継ぎシステム更新")
        
        print("\n🚀 すぐに作業開始:")
        print("  h 'システム状態確認'  ai '機能確認'  dashboard")
    
    def detail_handover(self):
        """詳細情報取得"""
        print("📊 HANAZONO詳細情報システム")
        print("=" * 40)
        
        for item in self.config["detail_items"]:
            if hasattr(self, f"get_{item}"):
                print(f"\n🔍 {item.replace('_', ' ').title()}:")
                getattr(self, f"get_{item}")()
    
    def update_system(self):
        """引き継ぎシステム更新"""
        print("🔄 引き継ぎシステム自動更新中...")
        
        # GitHub最新情報取得
        try:
            subprocess.run(['git', 'pull', 'origin', 'main'], 
                         cwd=self.base_dir, check=True)
            print("✅ GitHub同期完了")
        except:
            print("⚠️ GitHub同期スキップ")
        
        # システム情報更新
        self.update_handover_data()
        
        # 設定リフレッシュ
        self.load_config()
        
        print("✅ 引き継ぎシステム更新完了")
    
    # === 瞬間把握項目（カスタマイズ可能） ===
    
    def get_git_status(self):
        """Git状態確認"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.base_dir)
            changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            
            # 最新コミット
            commit_result = subprocess.run(['git', 'log', '-1', '--pretty=format:%h %s'], 
                                         capture_output=True, text=True, cwd=self.base_dir)
            latest_commit = commit_result.stdout.strip()
            
            print(f"📊 Git: {changes}件の未コミット変更")
            print(f"📝 最新: {latest_commit}")
            
        except Exception as e:
            print(f"📊 Git状態: 確認失敗 ({e})")
    
    def get_system_status(self):
        """システム状態確認"""
        try:
            # プロセス確認
            result = subprocess.run(['pgrep', '-f', 'python.*lvyuan'], 
                                  capture_output=True, text=True)
            processes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            
            # 最新データ確認
            data_dir = self.base_dir / "data"
            latest_data = "なし"
            if data_dir.exists():
                files = list(data_dir.glob("lvyuan_data_*.json"))
                if files:
                    latest_file = max(files, key=lambda f: f.stat().st_mtime)
                    mtime = datetime.fromtimestamp(latest_file.stat().st_mtime)
                    latest_data = mtime.strftime('%m-%d %H:%M')
            
            print(f"🔄 プロセス: {processes}個実行中")
            print(f"📈 最新データ: {latest_data}")
            
        except Exception as e:
            print(f"🔄 システム状態: 確認失敗 ({e})")
    
    def get_urgency_level(self):
        """緊急度自動判定"""
        urgency_score = 0
        issues = []
        
        # Git変更数チェック
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.base_dir)
            changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            
            if changes > 10:
                urgency_score += 3
                issues.append(f"大量の未コミット変更: {changes}件")
            elif changes > 5:
                urgency_score += 1
                issues.append(f"未コミット変更: {changes}件")
        except:
            pass
        
        # システムリソースチェック
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory().percent
            
            if cpu > 80:
                urgency_score += 2
                issues.append(f"高CPU使用率: {cpu}%")
            if memory > 80:
                urgency_score += 2
                issues.append(f"高メモリ使用率: {memory}%")
        except:
            pass
        
        # 緊急度判定
        if urgency_score >= 5:
            level = "🔴 高"
        elif urgency_score >= 2:
            level = "🟡 中"
        else:
            level = "✅ 低"
        
        print(f"⚠️ 緊急度: {level}")
        if issues:
            print(f"   問題: {', '.join(issues[:2])}")
    
    def get_available_commands(self):
        """利用可能コマンド"""
        commands = {
            "効率化": ["h 'システム状態確認'", "ai 'バグ修正'", "dashboard"],
            "Git管理": ["bash scripts/auto_git_organize_push.sh"],
            "監視": ["h 'アラート確認'", "h 'ライブ監視'"]
        }
        
        print("🛠️ 利用可能コマンド:")
        for category, cmds in commands.items():
            print(f"   {category}: {' | '.join(cmds[:2])}")
    
    def get_recommended_actions(self):
        """推奨アクション（AI自動判定）"""
        actions = []
        
        # Git状態に基づく推奨
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.base_dir)
            changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            
            if changes > 10:
                actions.append("Git整理実行推奨")
            elif changes > 0:
                actions.append("変更内容確認推奨")
        except:
            pass
        
        # システム状態に基づく推奨
        try:
            logs_dir = self.base_dir / "logs"
            if logs_dir.exists():
                recent_logs = list(logs_dir.glob("*.log"))
                if recent_logs:
                    actions.append("ログ確認推奨")
        except:
            pass
        
        if not actions:
            actions = ["システム正常 - 新機能開発可能"]
        
        print("🎯 AI推奨アクション:")
        for action in actions[:3]:
            print(f"   • {action}")
    
    # === 詳細情報項目（必要時のみ） ===
    
    def get_technical_specs(self):
        """技術仕様詳細"""
        specs = {
            "システム": "Raspberry Pi Zero 2W + LVYUAN SPI-10K-U",
            "バッテリー": "FLCD16-10048 × 4台 (20.48kWh)",
            "通信": "Modbus TCP (192.168.0.202:8899)",
            "言語": "Python 3.11 + Flask + psutil"
        }
        
        for key, value in specs.items():
            print(f"   {key}: {value}")
    
    def get_recent_changes(self):
        """最近の変更"""
        try:
            result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                                  capture_output=True, text=True, cwd=self.base_dir)
            changes = result.stdout.strip().split('\n')
            
            for change in changes:
                print(f"   • {change}")
        except:
            print("   変更履歴取得失敗")
    
    def get_error_logs(self):
        """エラーログ"""
        try:
            logs_dir = self.base_dir / "logs"
            if logs_dir.exists():
                recent_errors = []
                for log_file in list(logs_dir.glob("*.log"))[-3:]:
                    try:
                        with open(log_file) as f:
                            lines = f.readlines()[-20:]
                        
                        for line in lines:
                            if 'ERROR' in line or 'エラー' in line:
                                recent_errors.append(line.strip()[:80])
                    except:
                        continue
                
                if recent_errors:
                    for error in recent_errors[-3:]:
                        print(f"   • {error}")
                else:
                    print("   エラーなし")
            else:
                print("   ログディレクトリなし")
        except:
            print("   ログ確認失敗")
    
    def get_performance_metrics(self):
        """パフォーマンス指標"""
        try:
            import psutil
            
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            print(f"   CPU: {cpu}% | メモリ: {memory.percent}% | ディスク: {disk.percent}%")
        except:
            print("   メトリクス取得失敗")
    
    def get_full_documentation(self):
        """完全ドキュメント"""
        docs = [
            "AI_WORK_RULES.md", "PROJECT_STATUS.md", 
            "HANDOVER_PROMPT.md", "README.md"
        ]
        
        existing_docs = []
        for doc in docs:
            if (self.base_dir / doc).exists():
                existing_docs.append(doc)
        
        print(f"   利用可能ドキュメント: {', '.join(existing_docs)}")
        print(f"   確認コマンド: cat ~/lvyuan_solar_control/[ファイル名]")
    
    def update_handover_data(self):
        """引き継ぎデータ更新"""
        try:
            # GitHub自動情報取得実行
            result = subprocess.run(['bash', 'scripts/github_auto_fetch.sh'], 
                                  cwd=self.base_dir, capture_output=True)
            if result.returncode == 0:
                print("📊 GitHub情報更新完了")
            
            # システム状態更新
            result = subprocess.run(['bash', 'scripts/master_progress_controller.sh'], 
                                  cwd=self.base_dir, capture_output=True)
            if result.returncode == 0:
                print("🔄 システム状態更新完了")
                
        except Exception as e:
            print(f"⚠️ データ更新部分失敗: {e}")

def main():
    if len(sys.argv) == 1:
        # デフォルト: 瞬間把握
        hanazono = HANAZONOUltimate()
        hanazono.instant_handover()
    elif len(sys.argv) == 2:
        command = sys.argv[1]
        hanazono = HANAZONOUltimate()
        
        if command == "detail":
            hanazono.detail_handover()
        elif command == "update":
            hanazono.update_system()
        else:
            print(f"❓ 不明なコマンド: {command}")
            print("使用法: hanazono [detail|update]")
    else:
        print("使用法: hanazono [detail|update]")

if __name__ == "__main__":
    main()
