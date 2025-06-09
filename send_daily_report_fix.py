#!/usr/bin/env python3
"""
Send Daily Report Fix Script
目的: send_daily_report()の引数問題修復
原則: バックアップ前提・非破壊的・即座削除対象
"""

import shutil
from datetime import datetime

def analyze_send_daily_report():
    """send_daily_report メソッドの引数確認"""
    print("🔍 send_daily_report メソッド分析...")
    
    with open("email_notifier_v2_1.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # send_daily_report メソッドの定義を検索
    lines = content.splitlines()
    for i, line in enumerate(lines, 1):
        if "def send_daily_report" in line:
            print(f"📋 Line {i}: {line.strip()}")
            # 次の数行も表示
            for j in range(1, 5):
                if i + j < len(lines):
                    print(f"     {i+j}: {lines[i+j-1].strip()}")
            break
    
    return content

def fix_main_py_call():
    """main.py の send_daily_report 呼び出し修正"""
    print("🔧 main.py 引数修正...")
    
    # main.py バックアップ
    backup_file = f"main.py.backup_args_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2("main.py", backup_file)
    print(f"✅ main.py バックアップ: {backup_file}")
    
    # main.py 読み込み
    with open("main.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 問題箇所修正
    original_call = "success = notifier.send_daily_report(test_mode=not args.live)"
    
    # データ収集して渡す形に修正
    fixed_call = """# データ収集
        from collector_capsule import CollectorCapsule
        collector = CollectorCapsule()
        data = collector.get_latest_data()
        
        # メール送信
        success = notifier.send_daily_report(data, test_mode=not args.live)"""
    
    if original_call in content:
        content = content.replace(original_call, fixed_call)
        
        # ファイル書き込み
        with open("main.py", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ main.py 引数修正完了")
        return True
    else:
        print("⚠️ 対象行が見つかりません")
        return False

def test_fixed_execution():
    """修正後のテスト実行"""
    print("🧪 修正後テスト実行...")
    
    try:
        import subprocess
        result = subprocess.run(['python3', 'main.py', '--daily-report'], 
                              capture_output=True, text=True, timeout=60)
        
        print(f"📊 終了コード: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ 修正成功！")
        else:
            print("❌ まだエラーあり:")
            if result.stderr:
                for line in result.stderr.splitlines()[:5]:
                    print(f"   {line}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ テスト実行エラー: {e}")
        return False

def main():
    print("🔧 Send Daily Report Fix")
    print(f"実行時刻: {datetime.now()}")
    
    print("\n" + "="*60)
    print(" Phase 1: send_daily_report メソッド分析")
    print("="*60)
    analyze_send_daily_report()
    
    print("\n" + "="*60)
    print(" Phase 2: main.py 引数修正")
    print("="*60)
    fix_ok = fix_main_py_call()
    
    if fix_ok:
        print("\n" + "="*60)
        print(" Phase 3: 修正後テスト実行")
        print("="*60)
        test_ok = test_fixed_execution()
        
        if test_ok:
            print("\n🎉 HANAZONOメールシステム引数修復完了！")
        else:
            print("\n🔧 追加修正が必要です")

if __name__ == "__main__":
    main()
