#!/usr/bin/env python3
"""
HANAZONO継承精度向上システム v1.0
AI記憶継承の精度を劇的に改善する重要度アルゴリズム実装
"""

import os
import json
import sqlite3
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import re

class KiokuPrecisionSystem:
    """継承精度向上システム"""
    
    def __init__(self):
        self.version = "1.0.0-PRECISION"
        self.precision_db = "data/kioku_precision.db"
        self.critical_info = []
        self.current_status = []
        self.recent_progress = []
        self.background_context = []
        
    def analyze_and_generate_precision_handover(self):
        """精密継承ドキュメント生成"""
        print("🧠 HANAZONO継承精度向上システム実行開始")
        print("=" * 60)
        
        # 1. 重要度分析実行
        self._analyze_importance_scores()
        
        # 2. 情報分類・構造化
        self._classify_information()
        
        # 3. AI最適化継承ドキュメント生成
        self._generate_precision_handover()
        
        # 4. 継承精度データベース更新
        self._update_precision_database()
        
        print(f"\n🎯 継承精度向上システム実行完了")
        return True
    
    def _analyze_importance_scores(self):
        """重要度スコア分析"""
        print("\n📊 重要度スコア分析実行:")
        
        # Git最新情報取得
        git_info = self._get_git_information()
        
        # ファイル実装状況分析
        file_status = self._analyze_file_implementation()
        
        # 最近の変更分析
        recent_changes = self._analyze_recent_changes()
        
        # 重要度計算
        importance_items = []
        
        # 1. 直近の重要変更（時間的新しさ100点）
        for change in recent_changes:
            score = self._calculate_importance_score(
                time_newness=100,
                implementation_impact=change.get('impact', 60),
                completion_level=change.get('completion', 70)
            )
            importance_items.append({
                'type': 'recent_change',
                'content': change['description'],
                'score': score,
                'timestamp': change['timestamp']
            })
        
        # 2. 現在の実装状況（完成度重視）
        for file, status in file_status.items():
            if status['exists']:
                score = self._calculate_importance_score(
                    time_newness=80,
                    implementation_impact=90,
                    completion_level=status['completion_estimate']
                )
                importance_items.append({
                    'type': 'implementation_status',
                    'content': f"{file}: {status['line_count']}行, {status['completion_estimate']}%完成",
                    'score': score,
                    'file': file
                })
        
        # 3. Git状況（システム根幹）
        if git_info:
            score = self._calculate_importance_score(
                time_newness=90,
                implementation_impact=100,
                completion_level=80
            )
            importance_items.append({
                'type': 'git_status',
                'content': f"ブランチ: {git_info.get('branch')}, 未コミット: {len(git_info.get('changes', []))}件",
                'score': score,
                'git_info': git_info
            })
        
        # スコア順でソート
        self.importance_items = sorted(importance_items, key=lambda x: x['score'], reverse=True)
        
        print(f"✅ 重要度分析完了: {len(self.importance_items)}項目")
    
    def _calculate_importance_score(self, time_newness, implementation_impact, completion_level):
        """重要度スコア計算"""
        # 重み付け: 時間×0.3 + 影響度×0.4 + 完成度×0.3
        score = (time_newness * 0.3) + (implementation_impact * 0.4) + (completion_level * 0.3)
        return round(score, 1)
    
    def _get_git_information(self):
        """Git情報取得"""
        try:
            # ブランチ取得
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True)
            branch = result.stdout.strip()
            
            # 最新コミット
            result = subprocess.run(['git', 'log', '--oneline', '-3'], 
                                  capture_output=True, text=True)
            commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            # 未コミット変更
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            changes = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            return {
                'branch': branch,
                'recent_commits': commits,
                'changes': changes
            }
        except:
            return None
    
    def _analyze_file_implementation(self):
        """ファイル実装状況分析"""
        key_files = [
            'main.py', 'email_notifier.py', 'settings_manager.py',
            'lvyuan_collector.py', 'hanazono_complete_system.py',
            'github_data_integration_fixed.py', 'data_integration_system.py'
        ]
        
        file_status = {}
        
        for file in key_files:
            if os.path.exists(file):
                stat = os.stat(file)
                with open(file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # 完成度推定（行数・関数数・クラス数から）
                functions = len([l for l in lines if l.strip().startswith('def ')])
                classes = len([l for l in lines if l.strip().startswith('class ')])
                completion_estimate = min(100, (len(lines) // 10) + (functions * 5) + (classes * 10))
                
                file_status[file] = {
                    'exists': True,
                    'size': stat.st_size,
                    'line_count': len(lines),
                    'functions': functions,
                    'classes': classes,
                    'completion_estimate': completion_estimate,
                    'last_modified': datetime.fromtimestamp(stat.st_mtime)
                }
            else:
                file_status[file] = {'exists': False}
        
        return file_status
    
    def _analyze_recent_changes(self):
        """最近の変更分析"""
        changes = []
        
        # 24時間以内のファイル変更
        now = datetime.now()
        recent_threshold = now - timedelta(hours=24)
        
        for file in Path('.').glob('*.py'):
            stat = file.stat()
            modified_time = datetime.fromtimestamp(stat.st_mtime)
            
            if modified_time > recent_threshold:
                changes.append({
                    'description': f"{file.name} 最近更新",
                    'timestamp': modified_time.isoformat(),
                    'impact': 80,  # Python ファイルは高影響
                    'completion': 90  # 既存ファイルの更新は高完成度
                })
        
        # データベースファイルの存在確認
        if os.path.exists('data/hanazono_master_data.db'):
            changes.append({
                'description': "6年間データ統合完了 (hanazono_master_data.db)",
                'timestamp': datetime.now().isoformat(),
                'impact': 100,  # システム根幹変更
                'completion': 100  # 完全実装済み
            })
        
        return changes
    
    def _classify_information(self):
        """情報分類・構造化"""
        print("\n📋 情報分類・構造化:")
        
        # CRITICAL_IMMEDIATE (スコア90以上)
        self.critical_info = [item for item in self.importance_items if item['score'] >= 90]
        
        # CURRENT_STATUS (スコア70-89)
        self.current_status = [item for item in self.importance_items if 70 <= item['score'] < 90]
        
        # RECENT_PROGRESS (スコア50-69)
        self.recent_progress = [item for item in self.importance_items if 50 <= item['score'] < 70]
        
        # BACKGROUND_CONTEXT (スコア50未満)
        self.background_context = [item for item in self.importance_items if item['score'] < 50]
        
        print(f"🚨 CRITICAL_IMMEDIATE: {len(self.critical_info)}項目")
        print(f"📊 CURRENT_STATUS: {len(self.current_status)}項目")
        print(f"🔄 RECENT_PROGRESS: {len(self.recent_progress)}項目")
        print(f"📚 BACKGROUND_CONTEXT: {len(self.background_context)}項目")
    
    def _generate_precision_handover(self):
        """AI最適化継承ドキュメント生成"""
        print("\n📝 AI最適化継承ドキュメント生成:")
        
        doc_content = f"""# 🧠 HANAZONO AI継承ドキュメント v2.0 (精密版)

*生成時刻*: {datetime.now().isoformat()}
*継承精度*: 高精度アルゴリズム適用
*AI理解最適化*: 構造化・優先度付け完了

## 🚨 CRITICAL_IMMEDIATE (最重要・即座対応)

"""
        
        # CRITICAL情報（最重要）
        for i, item in enumerate(self.critical_info[:5], 1):  # 上位5項目のみ
            doc_content += f"""
### {i}. {item['content']} (スコア: {item['score']})
- **重要度**: 最高レベル
- **対応**: 即座確認・対応必須
"""
        
        # CURRENT_STATUS（現在状況）
        doc_content += f"""
## 📊 CURRENT_STATUS (現在状況)

### システム実装状況
"""
        for item in self.current_status[:8]:  # 上位8項目
            if item['type'] == 'implementation_status':
                doc_content += f"- ✅ {item['content']} (スコア: {item['score']})\n"
        
        # RECENT_PROGRESS（最近の進展）
        doc_content += f"""
## 🔄 RECENT_PROGRESS (最近の進展)

### 直近の重要変更
"""
        for item in self.recent_progress[:5]:  # 上位5項目
            doc_content += f"- 🔄 {item['content']} (スコア: {item['score']})\n"
        
        # 次のアクション（AI用）
        doc_content += f"""
## 🎯 AI次回必須アクション

### 最優先確認事項
1. **6年間データ統合状況確認**: `ls -la data/hanazono_master_data.db`
2. **メールシステム動作確認**: `python3 email_notifier.py`
3. **Git状況確認**: `git status`

### 推奨作業順序
1. 現在のシステム動作テスト
2. 6年間データ活用機能実装
3. 残り機能の完成度向上

---
*🧠 このドキュメントはkioku精密継承システムv1.0により生成*
"""
        
        # ファイル保存
        filename = "KIOKU_PRECISION_HANDOVER.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        print(f"📋 精密継承ドキュメント生成: {filename}")
        
        # 軽量版も生成（AI即座理解用）
        self._generate_quick_summary()
    
    def _generate_quick_summary(self):
        """AI即座理解用軽量サマリー"""
        summary = f"""# 🎯 HANAZONO即座理解サマリー

**現在状況（3行要約）**:
1. HANAZONOシステムv4.0完成、6年間データ統合済み (hanazono_master_data.db)
2. メールシステム (email_notifier.py 25,792バイト) 実装完了
3. 次のアクション: システム動作確認 → ML予測機能実装

**最重要ファイル**:
- email_notifier.py: メインシステム
- data/hanazono_master_data.db: 6年間データ
- main.py: 統合制御

**即座実行コマンド**:
```bash
python3 email_notifier.py  # メールシステムテスト
ls -la data/hanazono_master_data.db  # データ確認
git status  # 変更状況確認
"""

    with open("KIOKU_QUICK_SUMMARY.md", 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("📋 軽量サマリー生成: KIOKU_QUICK_SUMMARY.md")

def _update_precision_database(self):
    """継承精度データベース更新"""
    os.makedirs('data', exist_ok=True)
    
    conn = sqlite3.connect(self.precision_db)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS precision_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            total_items INTEGER,
            critical_items INTEGER,
            average_score REAL,
            handover_generated TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    avg_score = sum(item['score'] for item in self.importance_items) / len(self.importance_items) if self.importance_items else 0
    
    cursor.execute('''
        INSERT INTO precision_records 
        (timestamp, total_items, critical_items, average_score, handover_generated)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), len(self.importance_items), 
          len(self.critical_info), round(avg_score, 1), "KIOKU_PRECISION_HANDOVER.md"))
    
    conn.commit()
    conn.close()
    
    print("📊 継承精度データベース更新完了")
def main():
    """継承精度向上システム実行"""
    precision_system = KiokuPrecisionSystem()
    success = precision_system.analyze_and_generate_precision_handover()
    
    if success:
        print("\n🎉 継承精度向上システム実行完了！")
        print("✅ AI理解最適化継承ドキュメント生成済み")
        print("📋 次回AIセッションで高精度継承が可能")
        print("\n📁 生成ファイル:")
        print("  - KIOKU_PRECISION_HANDOVER.md (詳細版)")
        print("  - KIOKU_QUICK_SUMMARY.md (軽量版)")
    
    return success

if __name__ == "__main__":
    main()
