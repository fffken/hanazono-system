"""
設計思想違反検出・防止システム v1.0
全ての変更を監視し、設計思想違反を自動検出・阻止
"""

import os
import json
import subprocess
from datetime import datetime

class DesignViolationDetector:
    def __init__(self):
        self.core_principles = {
            "no_feature_deletion": "機能削除・無効化は絶対禁止",
            "no_regression": "確実な前進、絶対に後退なし", 
            "syntax_only_fix": "構文エラー = 構文のみ修正",
            "preserve_all_functions": "既存機能の完全保持"
        }
        
        self.critical_files = [
            "enhanced_email_system_v2.py",
            "email_notifier.py", 
            "ai_learning_database.py"
        ]
        
        self.forbidden_actions = [
            "削除", "delete", "remove", "無効", "disable",
            "コメントアウト", "# ", "劣化版", "短縮版"
        ]
    
    def check_before_modification(self, target_file, proposed_action):
        """変更前の強制チェック"""
        print(f"🛡️ 設計思想違反検出システム起動")
        print(f"📋 対象ファイル: {target_file}")
        print(f"📋 提案アクション: {proposed_action}")
        
        # 禁止アクション検出
        for forbidden in self.forbidden_actions:
            if forbidden in proposed_action.lower():
                print(f"🚨 設計思想違反検出: '{forbidden}'")
                print(f"❌ アクション拒否: {self.core_principles['no_feature_deletion']}")
                return False
        
        # 機能削除チェック
        if any(word in proposed_action.lower() for word in ["削除", "remove", "delete"]):
            print(f"🚨 機能削除検出")
            print(f"❌ 絶対禁止: {self.core_principles['preserve_all_functions']}")
            return False
            
        print(f"✅ 設計思想チェック通過")
        return True
    
    def suggest_alternatives(self, error_type):
        """代替案提案システム"""
        alternatives = {
            "syntax_error": [
                "1. nanoエディターでピンポイント修正",
                "2. 該当行のみを特定して修正", 
                "3. 機能は一切削除せず構文のみ修正",
                "4. バックアップから正常部分を抽出して統合"
            ],
            "import_error": [
                "1. 不足モジュールのインストール",
                "2. importパスの修正",
                "3. 機能削除ではなく依存関係修正"
            ]
        }
        
        print(f"💡 推奨代替案:")
        for alt in alternatives.get(error_type, ["詳細分析が必要"]):
            print(f"   {alt}")
    
    def emergency_protocol(self):
        """緊急時プロトコル"""
        print(f"""
🚨 緊急時プロトコル
━━━━━━━━━━━━━━━━━━━━
❌ 絶対禁止事項:
  - 機能削除・無効化
  - 劣化版への置き換え
  - コメントアウトによる無効化

✅ 許可される対応:
  - 構文エラーの修正のみ
  - 機能追加（削除は禁止）
  - ピンポイント修正

🔧 緊急時手順:
  1. 設計思想原則を再確認
  2. 代替案を3つ以上検討
  3. 機能保持を最優先
  4. 段階的修正実行
""")

if __name__ == "__main__":
    detector = DesignViolationDetector()
    detector.emergency_protocol()
