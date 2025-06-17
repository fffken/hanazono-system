#!/usr/bin/env python3
# 現状完成モジュール完全調査（完全非破壊的）
import datetime
import os
import glob
import json
import subprocess

def survey_completed_modules():
    """現状完成モジュール完全調査"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"📊 現状完成モジュール完全調査開始 {timestamp}")
    print("=" * 70)
    
    completed_modules = {}
    
    # 1. HANAZONOコアシステム確認
    print(f"🏗️ HANAZONOコアシステム:")
    
    core_files = [
        ("abc_integration_fixed_final_20250616_231158.py", "メインハブシステム"),
        ("weather_forecast.py", "天気予報システム"),
        ("main.py", "システム制御"),
    ]
    
    for file_path, description in core_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            mtime = os.path.getmtime(file_path)
            mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"  ✅ {description}: {file_path} ({file_size}バイト, {mtime_str})")
            
            # 機能確認
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # クラス・関数抽出
                import re
                classes = re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
                functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
                
                completed_modules[description] = {
                    "file": file_path,
                    "size": file_size,
                    "last_modified": mtime_str,
                    "classes": classes,
                    "functions": functions[:10],  # 最初の10個
                    "status": "完成"
                }
                
                print(f"    📋 クラス: {', '.join(classes)}")
                print(f"    🔧 主要関数: {', '.join(functions[:5])}")
                
            except Exception as e:
                print(f"    ❌ 内容確認エラー: {e}")
        else:
            print(f"  ❌ {description}: {file_path} (未発見)")
    
    # 2. データ収集システム確認
    print(f"\n📊 データ収集システム:")
    
    data_dir = "data"
    if os.path.exists(data_dir) and os.path.isdir(data_dir):
        data_files = glob.glob(f"{data_dir}/*.json")
        latest_data = max(data_files, key=lambda x: os.path.getctime(x)) if data_files else None
        
        if latest_data:
            data_mtime = os.path.getmtime(latest_data)
            data_time_str = datetime.datetime.fromtimestamp(data_mtime).strftime('%Y-%m-%d %H:%M:%S')
            age_hours = (datetime.datetime.now().timestamp() - data_mtime) / 3600
            
            print(f"  ✅ データ収集: {len(data_files)}ファイル")
            print(f"  📄 最新データ: {os.path.basename(latest_data)} ({data_time_str})")
            print(f"  ⏰ データ新鮮度: {age_hours:.1f}時間前")
            
            completed_modules["データ収集システム"] = {
                "total_files": len(data_files),
                "latest_file": latest_data,
                "freshness_hours": age_hours,
                "status": "稼働中"
            }
        else:
            print(f"  ❌ データファイル未発見")
    else:
        print(f"  ❌ データディレクトリ未発見")
    
    # 3. 自動化システム確認
    print(f"\n⚙️ 自動化システム:")
    
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            cron_content = result.stdout
            hanazono_crons = [line for line in cron_content.split('\n') 
                            if 'hanazono' in line.lower() or 'abc_integration' in line]
            
            print(f"  ✅ cron設定: {len(hanazono_crons)}個")
            for cron in hanazono_crons:
                if cron.strip():
                    print(f"    📅 {cron}")
            
            completed_modules["自動化システム"] = {
                "cron_jobs": len(hanazono_crons),
                "cron_lines": hanazono_crons,
                "status": "稼働中"
            }
        else:
            print(f"  ❌ cron確認失敗")
    except Exception as e:
        print(f"  ❌ cron確認エラー: {e}")
    
    # 4. ログ・監視システム確認
    print(f"\n📋 ログ・監視システム:")
    
    log_files = glob.glob('/tmp/hanazono_*.log')
    if log_files:
        recent_logs = sorted(log_files, key=lambda x: os.path.getmtime(x), reverse=True)
        
        print(f"  ✅ ログファイル: {len(log_files)}個")
        for log_file in recent_logs[:3]:
            log_mtime = os.path.getmtime(log_file)
            log_time_str = datetime.datetime.fromtimestamp(log_mtime).strftime('%H:%M:%S')
            print(f"    📄 {os.path.basename(log_file)} ({log_time_str})")
        
        completed_modules["ログ・監視システム"] = {
            "log_files": len(log_files),
            "recent_logs": [os.path.basename(f) for f in recent_logs[:5]],
            "status": "稼働中"
        }
    else:
        print(f"  ❌ ログファイル未発見")
    
    # 5. 追加モジュール探索
    print(f"\n🔍 追加モジュール探索:")
    
    all_py_files = glob.glob("*.py")
    additional_modules = []
    
    for py_file in all_py_files:
        if py_file not in [f[0] for f in core_files]:
            file_size = os.path.getsize(py_file)
            if file_size > 1000:  # 1KB以上のファイル
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 機能推定
                    if 'class' in content or 'def' in content:
                        import re
                        classes = re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
                        functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
                        
                        additional_modules.append({
                            "file": py_file,
                            "size": file_size,
                            "classes": len(classes),
                            "functions": len(functions)
                        })
                        
                except Exception:
                    pass
    
    print(f"  📋 追加Pythonモジュール: {len(additional_modules)}個")
    for module in additional_modules[:10]:  # 最初の10個
        print(f"    📄 {module['file']}: {module['size']}バイト, "
              f"{module['classes']}クラス, {module['functions']}関数")
    
    # 6. 完成モジュール要約
    print(f"\n" + "=" * 70)
    print(f"📊 完成モジュール要約:")
    print(f"=" * 70)
    
    total_modules = len(completed_modules)
    print(f"🏗️ コア完成モジュール: {total_modules}個")
    
    for module_name, module_info in completed_modules.items():
        status = module_info.get('status', '不明')
        print(f"  ✅ {module_name}: {status}")
    
    # 機能分類
    print(f"\n🎯 機能分類:")
    feature_categories = {
        "メール配信": ["メインハブシステム"],
        "天気予報": ["天気予報システム"],
        "データ収集": ["データ収集システム"],
        "自動化": ["自動化システム"],
        "監視": ["ログ・監視システム"]
    }
    
    for category, modules in feature_categories.items():
        available_modules = [m for m in modules if any(m in completed for completed in completed_modules.keys())]
        status = "✅ 完成" if available_modules else "❌ 未完成"
        print(f"  {status} {category}")
    
    # 7. 完成度評価
    completion_rate = (total_modules / 5) * 100  # 基本5モジュール想定
    print(f"\n🏆 システム完成度: {completion_rate:.1f}%")
    
    if completion_rate >= 100:
        print(f"🎉 基本システム完成！次の拡張機能実装準備完了")
    elif completion_rate >= 80:
        print(f"🔧 基本システムほぼ完成、残り作業わずか")
    else:
        print(f"⚠️ 基本システム構築継続中")
    
    # 結果保存
    survey_result = {
        "survey_date": timestamp,
        "completed_modules": completed_modules,
        "additional_modules": additional_modules,
        "completion_rate": completion_rate,
        "next_action": "拡張機能実装検討" if completion_rate >= 100 else "基本システム完成"
    }
    
    result_file = f"module_survey_{timestamp}.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(survey_result, f, indent=2, ensure_ascii=False)
    
    print(f"\n📝 調査結果保存: {result_file}")
    
    return completed_modules

if __name__ == "__main__":
    survey_completed_modules()
