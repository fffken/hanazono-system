#!/usr/bin/env python3
# 明後日天気予報消失原因徹底調査（完全非破壊的）
import datetime
import os
import json
import glob

def investigate_weather_missing():
    """明後日天気予報消失原因徹底調査"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🔍 明後日天気予報消失原因徹底調査開始 {timestamp}")
    print("=" * 70)
    
    # 1. 修正前後のファイル比較
    print(f"📄 修正前後ファイル比較:")
    
    backup_file = "backup_before_linebreak_fix_20250617_090232.py"
    current_file = "abc_integration_fixed_final_20250616_231158.py"
    
    # バックアップファイル確認
    if os.path.exists(backup_file):
        print(f"  ✅ 修正前ファイル: {backup_file}")
        
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            
            # 天気予報関連部分抽出
            backup_lines = backup_content.split('\n')
            weather_lines_backup = []
            
            for i, line in enumerate(backup_lines):
                if 'days[:3]' in line or 'weather_data[\'days\']' in line or '明後日' in line:
                    # 前後5行を含めて抽出
                    start = max(0, i-5)
                    end = min(len(backup_lines), i+6)
                    weather_lines_backup.extend(backup_lines[start:end])
                    weather_lines_backup.append("---")
            
            print(f"  📋 修正前の天気予報処理部分:")
            for line in weather_lines_backup[:20]:  # 最初の20行
                print(f"    {line}")
            
        except Exception as e:
            print(f"  ❌ 修正前ファイル読み取りエラー: {e}")
    else:
        print(f"  ❌ 修正前ファイル未発見: {backup_file}")
    
    # 現在のファイル確認
    if os.path.exists(current_file):
        print(f"\n  ✅ 修正後ファイル: {current_file}")
        
        try:
            with open(current_file, 'r', encoding='utf-8') as f:
                current_content = f.read()
            
            # 天気予報関連部分抽出
            current_lines = current_content.split('\n')
            weather_lines_current = []
            
            for i, line in enumerate(current_lines):
                if 'days[:3]' in line or 'weather_data[\'days\']' in line or '明後日' in line:
                    # 前後5行を含めて抽出
                    start = max(0, i-5)
                    end = min(len(current_lines), i+6)
                    weather_lines_current.extend(current_lines[start:end])
                    weather_lines_current.append("---")
            
            print(f"  📋 修正後の天気予報処理部分:")
            for line in weather_lines_current[:20]:  # 最初の20行
                print(f"    {line}")
            
        except Exception as e:
            print(f"  ❌ 修正後ファイル読み取りエラー: {e}")
    else:
        print(f"  ❌ 修正後ファイル未発見: {current_file}")
    
    # 2. 天気データソース確認
    print(f"\n🌤️ 天気データソース確認:")
    
    weather_file = "weather_forecast.py"
    if os.path.exists(weather_file):
        print(f"  ✅ 天気予報ファイル: {weather_file}")
        
        try:
            with open(weather_file, 'r', encoding='utf-8') as f:
                weather_content = f.read()
            
            # 天気データ取得部分確認
            weather_lines = weather_content.split('\n')
            
            # days配列関連確認
            days_lines = []
            for i, line in enumerate(weather_lines):
                if 'days' in line.lower() and ('append' in line or '=' in line or 'return' in line):
                    days_lines.append(f"行{i+1}: {line.strip()}")
            
            print(f"  📋 days配列処理:")
            for line in days_lines[:10]:  # 最初の10個
                print(f"    {line}")
            
            # 3日分データ確認
            three_day_indicators = ['3', 'three', '明後日', 'day_after_tomorrow']
            three_day_lines = []
            
            for i, line in enumerate(weather_lines):
                if any(indicator in line.lower() for indicator in three_day_indicators):
                    three_day_lines.append(f"行{i+1}: {line.strip()}")
            
            print(f"  📋 3日分データ関連:")
            for line in three_day_lines[:10]:  # 最初の10個
                print(f"    {line}")
                
        except Exception as e:
            print(f"  ❌ 天気ファイル読み取りエラー: {e}")
    else:
        print(f"  ❌ 天気予報ファイル未発見: {weather_file}")
    
    # 3. 実際の天気データ取得テスト
    print(f"\n🧪 実際の天気データ取得テスト:")
    
    try:
        # 現在のシステムから天気データ取得
        import sys
        sys.path.insert(0, '.')
        
        import importlib.util
        spec = importlib.util.spec_from_file_location("current_system", current_file)
        current_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(current_module)
        
        # システムインスタンス作成
        if hasattr(current_module, 'IntegrateBattleToMail'):
            system = current_module.IntegrateBattleToMail()
            
            # 天気データ取得
            weather_data = system.get_perfect_weather_data()
            
            print(f"  📊 取得された天気データ:")
            print(f"    データ型: {type(weather_data)}")
            
            if isinstance(weather_data, dict) and 'days' in weather_data:
                days = weather_data['days']
                print(f"    days配列長: {len(days)}")
                
                for i, day in enumerate(days):
                    day_label = ['今日', '明日', '明後日'][i] if i < 3 else f'Day{i+1}'
                    print(f"    {day_label}: {day.get('display_date', '不明')} - {day.get('weather', '不明')[:30]}...")
                    
                if len(days) < 3:
                    print(f"  ⚠️ 明後日データ不足: {len(days)}日分のみ")
                else:
                    print(f"  ✅ 3日分データ正常取得")
            else:
                print(f"  ❌ 天気データ構造異常: {weather_data}")
                
        else:
            print(f"  ❌ システムクラス未発見")
            
    except Exception as e:
        print(f"  ❌ 天気データ取得テスト失敗: {e}")
    
    # 4. メール送信部分の天気表示ロジック確認
    print(f"\n📧 メール送信天気表示ロジック確認:")
    
    try:
        with open(current_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # メール送信関数内の天気処理部分を特定
        in_email_function = False
        weather_processing_lines = []
        
        for i, line in enumerate(lines):
            if 'send_battle_integrated_email' in line:
                in_email_function = True
            
            if in_email_function:
                if 'for i, day in enumerate' in line and 'weather_data' in line:
                    # この部分から数行を抽出
                    start = i
                    end = min(len(lines), i + 15)
                    weather_processing_lines = lines[start:end]
                    break
        
        print(f"  📋 メール送信内天気処理:")
        for i, line in enumerate(weather_processing_lines):
            print(f"    {i+1}: {line}")
            
    except Exception as e:
        print(f"  ❌ メール送信ロジック確認エラー: {e}")
    
    # 5. 原因推定と解決策提案
    print(f"\n" + "=" * 70)
    print(f"🎯 原因推定と解決策:")
    print(f"=" * 70)
    
    print(f"🔍 推定原因:")
    print(f"1. 改行修正時にループ範囲が変更された可能性")
    print(f"2. 天気データ取得で3日分取得できていない可能性")
    print(f"3. メール表示ループで明後日部分がスキップされている可能性")
    
    print(f"\n🛠️ 推奨解決アクション:")
    print(f"1. 天気データ取得確認・修正")
    print(f"2. メール表示ループ範囲修正")
    print(f"3. 修正版テスト・確認")
    
    return True

if __name__ == "__main__":
    investigate_weather_missing()
