#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path
import subprocess

def verify_ticket():
    """セキュリティチケット検証"""
    ticket_files = list(Path("security_clearance/execution_tickets").glob("ticket_auto_code_fixes.py_*.json"))
    if not ticket_files:
        print("❌ 実行チケットが見つかりません")
        return False
    
    with open(ticket_files[0], 'r') as f:
        ticket_data = json.load(f)
    
    # 有効期限確認
    expiry = datetime.fromisoformat(ticket_data['expiry_timestamp'])
    if datetime.now() > expiry:
        print("❌ 実行チケットが期限切れです")
        return False
    
    # 実行回数確認
    if ticket_data['execution_count'] >= ticket_data['max_executions']:
        print("❌ 実行回数上限に達しています")
        return False
    
    # 実行回数更新
    ticket_data['execution_count'] += 1
    with open(ticket_files[0], 'w') as f:
        json.dump(ticket_data, f, indent=2)
    
    remaining = ticket_data['max_executions'] - ticket_data['execution_count']
    print(f"✅ セキュリティチケット検証成功 (残り{remaining}回)")
    return True

def main():
    """セキュア実行メイン"""
    if not verify_ticket():
        exit(1)
    
    print("🔐 セキュアモードで auto_code_fixes.py を実行")
    result = subprocess.run(['python3', 'auto_code_fixes.py'])
    return result.returncode

if __name__ == "__main__":
    exit(main())
