#!/usr/bin/env python3
"""
簡単なkioku修正スクリプト
"""

def create_working_kioku():
    """動作するkiokuシステム作成"""
    print("🔧 動作版kiokuシステム作成中...")
    
    code = '''#!/usr/bin/env python3
"""
HANAZONO継承精度システム v1.0 (動作版)
"""
import os
import subprocess
from datetime import datetime

def generate_precision_handover():
    print("🧠 継承精度向上システム実行")
    
    # Git情報取得
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        changes = len(result.stdout.strip().split('\\n')) if result.stdout.strip() else 0
    except:
        changes = 0
    
    # ファイル確認
    important_files = {
        'email_notifier.py': os.path.exists('email_notifier.py'),
        'main.py': os.path.exists('main.py'),
        'data/hanazono_master_data.db': os.path.exists('data/hanazono_master_data.db')
    }
    
    # 継承ドキュメント生成
    content = f"""# 🧠 HANAZONO継承ドキュメント v2.0

*生成時刻*: {datetime.now().isoformat()}

## 🚨 最重要情報

### システム状況
- 未コミット変更: {changes}件
- HANAZONOシステム: v4.0完成状態

### 重要ファイル
"""
    
    for file, exists in important_files.items():
        status = "✅ 存在" if exists else "❌ 未存在"
        content += f"- {file}: {status}\\n"
    
    content += """
## 🎯 次回AI必須アクション

1. システムテスト: `python3 email_notifier.py`
2. データ確認: `ls -la data/hanazono_master_data.db`
3. Git確認: `git status`

---
*継承精度システムv1.0生成*
"""
    
    with open('KIOKU_PRECISION_HANDOVER.md', 'w') as f:
        f.write(content)
    
    print("✅ 継承ドキュメント生成完了")
    return True

if __name__ == "__main__":
    generate_precision_handover()
'''
    
    with open('kioku_precision_working.py', 'w') as f:
        f.write(code)
    
    print("✅ 動作版作成完了")

if __name__ == "__main__":
    create_working_kioku()
