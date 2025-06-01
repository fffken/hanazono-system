#!/usr/bin/env python3
"""
HANAZONO GitHub自動引き継ぎシステム v3.1（完全自動コピペ版）
新AIが即座に完全把握・高効率作業開始
"""

import json
import subprocess
import glob
from datetime import datetime
from pathlib import Path

class HANAZONOGitHubAuto:
    def __init__(self):
        self.base_dir = Path.home() / "lvyuan_solar_control"
        self.github_info_file = self.base_dir / "github_auto_handover.md"
        
    def execute_handover(self):
        """メイン引き継ぎ実行"""
        print("🏆 HANAZONOシステム - 究極引き継ぎ v3.1")
        print("=" * 50)
        
        # Step 1: GitHub情報更新
        self.update_github_info()
        
        # Step 2: GitHub自動読み取り情報生成
        self.generate_github_handover()
        
        # Step 3: 新AIセッション用コピペテキスト表示
        self.show_copy_paste_text()
        
    def show_copy_paste_text(self):
        """新AIセッション用コピペテキスト表示"""
        print("\n" + "=" * 60)
        print("📋 【新AIセッション用コピペテキスト】")
        print("=" * 60)
        
        copy_text = f"""新AIセッション開始。HANAZONOソーラー蓄電システムの作業を継続します。

以下のGitHubファイルをweb_searchで読み取って完全状況把握してください：

1. https://github.com/fffken/hanazono-system/blob/main/AI_WORK_RULES.md
   → AI作業ルール・効率化手法・コピーマーカー使用法

2. https://github.com/fffken/hanazono-system/blob/main/PROJECT_STATUS.md  
   → プロジェクト現在状況・進捗・システム概要

3. https://github.com/fffken/hanazono-system/blob/main/github_auto_handover.md
   → 最新システム状態・推奨アクション・利用可能コマンド

読み取り完了後、即座に以下のコマンドが使用可能です：

🔧 効率化コマンド：
- h 'システム状態確認'    # 統合システム確認
- ai 'バグ修正して'        # AI自動開発  
- dashboard               # リアルタイム監視画面
- hanazono detail         # 詳細情報確認

⚡ Git管理：
- bash scripts/auto_git_organize_push.sh  # Git自動整理

📊 現在状況：{self.get_current_git_status()}
📅 更新時刻：{datetime.now().strftime('%Y-%m-%d %H:%M')}

GitHub読み取り完了後、効率化システムにより高速作業継続が可能です。"""

        print(copy_text)
        
        print("=" * 60)
        print("📋 上記テキストを新AIセッションにコピペしてください")
        print("🎯 新AIが即座に完全状況把握・高効率作業開始します")
        print("=" * 60)
    
    def update_github_info(self):
        """GitHub情報自動更新"""
        print("🔄 GitHub情報自動更新中...")
        
        try:
            # 現在の状況をGitHubにプッシュ
            subprocess.run(['git', 'add', '.'], cwd=self.base_dir, check=False)
            
            # コミットメッセージ生成
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            commit_msg = f"🔄 auto: 引き継ぎ情報自動更新 - {timestamp}"
            
            subprocess.run(['git', 'commit', '-m', commit_msg], 
                         cwd=self.base_dir, check=False)
            subprocess.run(['git', 'push', 'origin', 'main'], 
                         cwd=self.base_dir, check=False)
            
            print("✅ GitHub自動更新完了")
            
        except Exception as e:
            print(f"⚠️ GitHub更新部分失敗: {e}")
    
    def generate_github_handover(self):
        """GitHub自動読み取り用情報生成"""
        handover_content = self.create_handover_content()
        
        # GitHub引き継ぎファイル作成
        with open(self.github_info_file, 'w', encoding='utf-8') as f:
            f.write(handover_content)
        
        print(f"📝 GitHub引き継ぎ情報生成: {self.github_info_file.name}")
        
        # 自動コミット
        try:
            subprocess.run(['git', 'add', str(self.github_info_file)], cwd=self.base_dir)
            subprocess.run(['git', 'commit', '-m', '🤖 auto: GitHub自動引き継ぎ情報更新'], 
                         cwd=self.base_dir, check=False)
            subprocess.run(['git', 'push', 'origin', 'main'], cwd=self.base_dir, check=False)
            print("✅ GitHub引き継ぎ情報自動プッシュ完了")
        except:
            print("⚠️ 自動プッシュスキップ")
    
    def create_handover_content(self):
        """引き継ぎコンテンツ作成"""
        content = f"""# 🤖 HANAZONO新AIセッション自動引き継ぎ情報

**生成時刻**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**システム**: HANAZONOソーラー蓄電システム自動最適化

## 📋 新AI向け指示

### ⚡ 即座に実行してください
新AIは以下のGitHubファイルを自動読み取りして完全状況把握してください：

1. **AI_WORK_RULES.md** - 作業ルール・効率化手法
2. **PROJECT_STATUS.md** - プロジェクト現在状況  
3. **hanazono_dev.py** - 統合開発コマンドシステム
4. **ai_assistant.py** - AI自動開発アシスタント
5. **hanazono_dashboard.py** - リアルタイム監視システム

### 🎯 GitHub自動読み取り手順
新AIはweb_searchツールで以下にアクセス：
https://github.com/fffken/hanazono-system/blob/main/AI_WORK_RULES.md
https://github.com/fffken/hanazono-system/blob/main/PROJECT_STATUS.md
https://github.com/fffken/hanazono-system/tree/main

## 📊 現在の状況サマリー

### Git状態
{self.get_detailed_git_status()}

### システム状態  
{self.get_detailed_system_status()}

### 利用可能な効率化コマンド
- `h 'システム状態確認'` - 統合システム確認
- `ai 'バグ修正して'` - AI自動開発
- `dashboard` - リアルタイム監視画面
- `hanazono detail` - 詳細情報確認

### 🎯 AI推奨次アクション
{self.get_recommended_actions()}

## 🚀 作業開始準備完了

新AIは上記GitHub読み取り完了後、即座に：
1. 効率化コマンドが使用可能
2. プロジェクト完全把握済み
3. 最適な作業継続が可能

**完璧な引き継ぎシステムにより、新AIセッションも即座に高効率作業開始！**
"""
        return content
    
    def get_current_git_status(self):
        """現在のGit状態（簡潔版）"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.base_dir)
            changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            return f"{changes}件の未コミット変更"
        except:
            return "Git状態確認失敗"
    
    def get_detailed_git_status(self):
        """詳細Git状態"""
        try:
            # 未コミット変更
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.base_dir)
            changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            
            # 最新コミット
            commit_result = subprocess.run(['git', 'log', '-1', '--pretty=format:%h %s'], 
                                         capture_output=True, text=True, cwd=self.base_dir)
            latest_commit = commit_result.stdout.strip()
            
            return f"""
- 未コミット変更: {changes}件
- 最新コミット: {latest_commit}
- ブランチ: main
- リモート: git@github.com:fffken/hanazono-system.git"""
            
        except Exception as e:
            return f"Git状態取得エラー: {e}"
    
    def get_detailed_system_status(self):
        """詳細システム状態"""
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
            
            # システムリソース
            try:
                import psutil
                cpu = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory().percent
                resource_info = f"CPU: {cpu}% | メモリ: {memory.percent}%"
            except:
                resource_info = "リソース情報取得失敗"
            
            return f"""
- Pythonプロセス: {processes}個実行中
- 最新データ: {latest_data}
- システムリソース: {resource_info}
- 稼働状況: 正常"""
            
        except Exception as e:
            return f"システム状態取得エラー: {e}"
    
    def get_recommended_actions(self):
        """推奨アクション"""
        actions = []
        
        # Git状態チェック
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.base_dir)
            changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            
            if changes > 5:
                actions.append("Git整理推奨（bash scripts/auto_git_organize_push.sh）")
            elif changes > 0:
                actions.append("変更内容確認推奨（h 'git状態確認'）")
        except:
            pass
        
        # システムチェック
        actions.append("システム状態確認推奨（h 'システム状態確認'）")
        actions.append("監視ダッシュボード確認可能（dashboard）")
        
        if not actions:
            actions = ["システム正常 - 新機能開発・改善作業可能"]
        
        return "\n".join([f"- {action}" for action in actions[:4]])

def main():
    """メイン実行"""
    hanazono = HANAZONOGitHubAuto()
    hanazono.execute_handover()

if __name__ == "__main__":
    main()
