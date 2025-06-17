#!/usr/bin/env python3
# システム問題点完全把握（完全非破壊的）
import datetime
import os
import subprocess
import json
import glob

def analyze_system_problems():
    """システム問題点完全把握"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🔍 システム問題点完全把握開始 {timestamp}")
    print("=" * 70)
    
    problems = []
    
    # 1. cronファイル状況確認
    cron_file = "abc_integration_fixed_final_20250616_231158.py"
    print(f"📄 cronファイル状況確認:")
    
    if os.path.exists(cron_file):
        cron_size = os.path.getsize(cron_file)
        print(f"  ✅ {cron_file}: {cron_size}バイト")
        
        # cronファイル内容確認
        try:
            with open(cron_file, 'r', encoding='utf-8') as f:
                cron_content = f.read()
            
            # 重要機能の存在確認
            functions_check = {
                "format_battle_section": "format_battle_section" in cron_content,
                "send_email": "send_email" in cron_content or "send_" in cron_content,
                "get_weather": "get_weather" in cron_content or "weather" in cron_content,
                "battery_data": "battery" in cron_content,
                "main_function": "__main__" in cron_content
            }
            
            print(f"  🔧 機能確認:")
            for func, exists in functions_check.items():
                status = "✅" if exists else "❌"
                print(f"    {func}: {status}")
                if not exists:
                    problems.append(f"cronファイル機能不足: {func}")
                    
        except Exception as e:
            print(f"  ❌ cronファイル読み取りエラー: {e}")
            problems.append(f"cronファイル読み取り不可: {e}")
    else:
        print(f"  ❌ cronファイル未発見: {cron_file}")
        problems.append(f"cronファイル未発見: {cron_file}")
    
    # 2. cron設定確認
    print(f"\n⚙️ cron設定確認:")
    try:
        result = subprocess.run(['crontab', '-l'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            cron_content = result.stdout
            print(f"  📋 cron設定内容:")
            lines = cron_content.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    print(f"    {line}")
            
            # HANAZONOシステム関連のcron確認
            hanazono_crons = [line for line in lines if 'abc_integration' in line or 'hanazono' in line.lower()]
            if hanazono_crons:
                print(f"  ✅ HANAZONOシステムcron: {len(hanazono_crons)}個")
            else:
                print(f"  ❌ HANAZONOシステムcron未設定")
                problems.append("HANAZONOシステムcron未設定")
        else:
            print(f"  ❌ cron確認エラー: {result.stderr}")
            problems.append(f"cron確認不可: {result.stderr}")
    except Exception as e:
        print(f"  ❌ cron確認例外: {e}")
        problems.append(f"cron確認例外: {e}")
    
    # 3. 依存ファイル確認
    print(f"\n📁 依存ファイル確認:")
    required_files = [
        "weather_forecast.py",
        "main.py",
        "data/",
    ]
    
    for req_file in required_files:
        if os.path.exists(req_file):
            if os.path.isdir(req_file):
                file_count = len(os.listdir(req_file))
                print(f"  ✅ {req_file}: {file_count}ファイル")
            else:
                file_size = os.path.getsize(req_file)
                print(f"  ✅ {req_file}: {file_size}バイト")
        else:
            print(f"  ❌ {req_file}: 未発見")
            problems.append(f"依存ファイル未発見: {req_file}")
    
    # 4. 最新データファイル確認
    print(f"\n📊 最新データファイル確認:")
    try:
        data_files = glob.glob('data/collected_data_*.json')
        if data_files:
            latest_data = max(data_files, key=lambda x: os.path.getctime(x))
            data_mtime = os.path.getmtime(latest_data)
            data_time_str = datetime.datetime.fromtimestamp(data_mtime).strftime('%Y-%m-%d %H:%M:%S')
            print(f"  ✅ 最新データ: {latest_data} ({data_time_str})")
            
            # データ新しさ確認
            now = datetime.datetime.now()
            data_time = datetime.datetime.fromtimestamp(data_mtime)
            age_hours = (now - data_time).total_seconds() / 3600
            
            if age_hours > 24:
                print(f"  ⚠️ データ古い: {age_hours:.1f}時間前")
                problems.append(f"データ古い: {age_hours:.1f}時間前")
            else:
                print(f"  ✅ データ新鮮: {age_hours:.1f}時間前")
        else:
            print(f"  ❌ データファイル未発見")
            problems.append("データファイル未発見")
    except Exception as e:
        print(f"  ❌ データ確認エラー: {e}")
        problems.append(f"データ確認エラー: {e}")
    
    # 5. メール送信テスト（実際には送信しない）
    print(f"\n📧 メール機能確認:")
    if os.path.exists(cron_file):
        try:
            # cronファイルをインポートしてテスト
            import importlib.util
            spec = importlib.util.spec_from_file_location("cron_module", cron_file)
            cron_module = importlib.util.module_from_spec(spec)
            
            # クラス確認
            if hasattr(cron_module, '__dict__'):
                classes = [name for name, obj in cron_module.__dict__.items() 
                          if isinstance(obj, type)]
                print(f"  📋 利用可能クラス: {classes}")
                
                # メール関連メソッド確認
                mail_methods = []
                for class_name in classes:
                    class_obj = getattr(cron_module, class_name)
                    methods = [method for method in dir(class_obj) 
                             if 'mail' in method.lower() or 'send' in method.lower()]
                    mail_methods.extend(methods)
                
                if mail_methods:
                    print(f"  ✅ メール関連メソッド: {mail_methods}")
                else:
                    print(f"  ❌ メール関連メソッド未発見")
                    problems.append("メール関連メソッド未発見")
            else:
                print(f"  ❌ モジュール構造確認不可")
                problems.append("モジュール構造確認不可")
                
        except Exception as e:
            print(f"  ❌ メール機能確認エラー: {e}")
            problems.append(f"メール機能確認エラー: {e}")
    
    # 6. Git状態確認
    print(f"\n🔄 Git状態確認:")
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            changes = result.stdout.strip()
            if changes:
                change_lines = changes.split('\n')
                print(f"  📊 未コミット変更: {len(change_lines)}ファイル")
                for line in change_lines[:5]:  # 最初の5個表示
                    print(f"    {line}")
                if len(change_lines) > 5:
                    print(f"    ... 他{len(change_lines) - 5}個")
            else:
                print(f"  ✅ Git状態クリーン")
        else:
            print(f"  ❌ Git状態確認エラー")
            problems.append("Git状態確認不可")
    except Exception as e:
        print(f"  ❌ Git確認例外: {e}")
        problems.append(f"Git確認例外: {e}")
    
    # 7. 問題点まとめ
    print(f"\n" + "=" * 70)
    print(f"🚨 発見された問題点:")
    print(f"=" * 70)
    
    if problems:
        for i, problem in enumerate(problems, 1):
            print(f"{i:2d}. {problem}")
    else:
        print(f"✅ 重大な問題は発見されませんでした")
    
    print(f"\n📊 問題点数: {len(problems)}")
    
    # 8. 問題点記録保存
    problem_record = {
        "analysis_time": timestamp,
        "total_problems": len(problems),
        "problems": problems,
        "system_status": "problematic" if problems else "healthy"
    }
    
    record_file = f"system_problems_{timestamp}.json"
    with open(record_file, 'w', encoding='utf-8') as f:
        json.dump(problem_record, f, indent=2, ensure_ascii=False)
    
    print(f"📝 問題点記録: {record_file}")
    
    return problems

if __name__ == "__main__":
    analyze_system_problems()
