#!/usr/bin/env python3
"""緊急修正スクリプト"""

def create_simple_working_kioku():
    print("🔧 簡単動作版kioku作成中...")
    
    code = '''#!/usr/bin/env python3
"""
HANAZONO究極kiokuシステム v3.0 (簡単動作版)
"""
import os
import subprocess
from datetime import datetime

def generate_ultimate_handover():
    print("🧠 究極kiokuシステム v3.0 実行開始")
    print("=" * 60)
    
    # 情報収集
    info = collect_information()
    
    # 3秒継承ドキュメント生成
    handover_3sec = create_3sec_handover(info)
    
    # 詳細版生成
    handover_detail = create_detail_handover(info)
    
    # 保存
    save_documents(handover_3sec, handover_detail)
    
    print("🎉 究極継承ドキュメント生成完了")

def collect_information():
    info = []
    
    # Git状況
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        changes = len(result.stdout.strip().split('\\n')) if result.stdout.strip() else 0
        info.append(f"Git未コミット変更: {changes}件")
    except:
        info.append("Git状況: 確認不可")
    
    # 重要ファイル
    files = ['email_notifier.py', 'main.py', 'data/hanazono_master_data.db']
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            info.append(f"{file}: {size}バイト")
        else:
            info.append(f"{file}: 未存在")
    
    return info
