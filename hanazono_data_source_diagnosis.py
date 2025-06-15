#!/usr/bin/env python3
# HANAZONOデータソース完全診断 - 原因特定と解決
import os
import json
import subprocess
import datetime

def complete_data_source_diagnosis():
    """全データソースの完全診断"""
    
    print("🔍 HANAZONOデータソース完全診断開始")
    print("=" * 50)
    
    diagnosis_results = {}
    
    # 1. ファイル存在確認
    print("📋 1. データファイル存在確認")
    files_to_check = [
        'data/capsule_data.json',
        'collector_capsule.py',
        'weather_forecast.py',
        'logs/hanazono_morning.log',
        'logs/hanazono_evening.log',
        'logs/collector_capsule.log'
    ]
    
    for file_path in files_to_check:
        exists = os.path.exists(file_path)
        print(f"  {'✅' if exists else '❌'} {file_path}")
        diagnosis_results[file_path] = exists
        
        if exists and file_path.endswith('.json'):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        print(f"    📊 データ件数: {len(data)}件")
                        if data:
                            print(f"    📅 最新データ: {data[-1].get('timestamp', '不明')}")
                    else:
                        print(f"    📊 データ形式: {type(data)}")
            except Exception as e:
                print(f"    ❌ 読み込みエラー: {e}")
    
    # 2. CollectorCapsule直接実行テスト
    print("\n📋 2. CollectorCapsule直接実行テスト")
    try:
        result = subprocess.run(['python3', 'collector_capsule.py'], 
                              capture_output=True, text=True, timeout=10)
        print(f"  終了コード: {result.returncode}")
        print(f"  標準出力: {result.stdout[:200]}...")
        if result.stderr:
            print(f"  エラー出力: {result.stderr[:200]}...")
        diagnosis_results['collector_capsule_execution'] = result.returncode == 0
    except subprocess.TimeoutExpired:
        print("  ❌ タイムアウト（10秒）")
        diagnosis_results['collector_capsule_execution'] = False
    except Exception as e:
        print(f"  ❌ 実行エラー: {e}")
        diagnosis_results['collector_capsule_execution'] = False
    
    # 3. 天気予報モジュール実行テスト
    print("\n📋 3. 天気予報モジュール実行テスト")
    try:
        result = subprocess.run(['python3', 'weather_forecast.py'], 
                              capture_output=True, text=True, timeout=10)
        print(f"  終了コード: {result.returncode}")
        print(f"  標準出力: {result.stdout[:200]}...")
        if result.stderr:
            print(f"  エラー出力: {result.stderr[:200]}...")
        diagnosis_results['weather_forecast_execution'] = result.returncode == 0
    except subprocess.TimeoutExpired:
        print("  ❌ タイムアウト（10秒）")
        diagnosis_results['weather_forecast_execution'] = False
    except Exception as e:
        print(f"  ❌ 実行エラー: {e}")
        diagnosis_results['weather_forecast_execution'] = False
    
    # 4. 最新ログ内容確認
    print("\n📋 4. 最新ログ内容確認")
    log_files = ['logs/collector_capsule.log', 'logs/hanazono_morning.log']
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    print(f"  📁 {log_file}: {len(lines)}行")
                    if lines:
                        print(f"    最新行: {lines[-1].strip()}")
                        # SOCやバッテリーデータを検索
                        soc_lines = [line for line in lines[-10:] if 'SOC' in line or 'soc' in line]
                        if soc_lines:
                            print(f"    SOCデータ: {soc_lines[-1].strip()}")
            except Exception as e:
                print(f"    ❌ 読み込みエラー: {e}")
    
    # 5. 直接Modbusテスト
    print("\n📋 5. 直接Modbusアクセステスト")
    try:
        # main.pyやModbus関連モジュールの確認
        modbus_files = ['main.py', 'modbus_client.py', 'solar_data_collector.py']
        for modbus_file in modbus_files:
            if os.path.exists(modbus_file):
                print(f"  ✅ {modbus_file} 存在")
                # 直接実行テスト
                try:
                    if modbus_file == 'main.py':
                        result = subprocess.run(['python3', 'main.py', '--live'], 
                                              capture_output=True, text=True, timeout=5)
                        if result.stdout:
                            print(f"    出力: {result.stdout[:100]}...")
                except subprocess.TimeoutExpired:
                    print(f"    ⚠️ {modbus_file} タイムアウト（通常動作）")
                except Exception as e:
                    print(f"    ❌ {modbus_file} エラー: {e}")
            else:
                print(f"  ❌ {modbus_file} 未発見")
    except Exception as e:
        print(f"  ❌ Modbusテストエラー: {e}")
    
    # 6. 代替データソース探索
    print("\n📋 6. 代替データソース探索")
    alternative_sources = [
        'data/',
        'logs/',
        'backup/',
        'system_backups/'
    ]
    
    for source_dir in alternative_sources:
        if os.path.exists(source_dir):
            files = os.listdir(source_dir)
            json_files = [f for f in files if f.endswith('.json')]
            log_files = [f for f in files if f.endswith('.log')]
            
            print(f"  📁 {source_dir}: {len(files)}ファイル")
            if json_files:
                print(f"    JSON: {json_files[:3]}{'...' if len(json_files) > 3 else ''}")
            if log_files:
                print(f"    LOG: {log_files[:3]}{'...' if len(log_files) > 3 else ''}")
    
    # 7. 診断結果まとめと解決策提示
    print("\n📋 7. 診断結果まとめ")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    working_sources = []
    failed_sources = []
    
    for source, status in diagnosis_results.items():
        if status:
            working_sources.append(source)
        else:
            failed_sources.append(source)
    
    print(f"✅ 動作中: {len(working_sources)}項目")
    for source in working_sources:
        print(f"  ✅ {source}")
    
    print(f"\n❌ 問題あり: {len(failed_sources)}項目")
    for source in failed_sources:
        print(f"  ❌ {source}")
    
    # 8. 具体的解決策提示
    print("\n📋 8. 具体的解決策")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    if not diagnosis_results.get('data/capsule_data.json', False):
        print("🔧 CollectorCapsuleデータ修復:")
        print("  1. python3 collector_capsule.py を手動実行")
        print("  2. データ出力確認")
        print("  3. JSONファイル生成確認")
    
    if not diagnosis_results.get('collector_capsule_execution', True):
        print("🔧 CollectorCapsule実行修復:")
        print("  1. 依存関係確認")
        print("  2. 権限確認")
        print("  3. ネットワーク接続確認")
    
    if not diagnosis_results.get('weather_forecast_execution', True):
        print("🔧 天気予報モジュール修復:")
        print("  1. APIキー確認")
        print("  2. インターネット接続確認")
        print("  3. 代替天気データソース検討")
    
    print(f"\n🎉 診断完了 - {datetime.datetime.now()}")
    return diagnosis_results

if __name__ == "__main__":
    results = complete_data_source_diagnosis()
    print("\n📋 次のステップ:")
    print("1. 上記の解決策を実行")
    print("2. 修復後に再度メール送信テスト")
    print("3. 実データ取得成功まで段階的修正")
