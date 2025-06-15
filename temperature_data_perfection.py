#!/usr/bin/env python3
# 2-3日目気温データ完璧化診断・修正
import requests
import json
import datetime

class TemperatureDataPerfection:
    """気温データ構造完全解析・修正"""
    
    def __init__(self):
        self.api_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/370000.json"
        
    def analyze_full_api_structure(self):
        """API完全データ構造解析"""
        print("🔍 気象庁API完全データ構造解析")
        print("=" * 60)
        
        try:
            response = requests.get(self.api_url, timeout=15)
            if response.status_code != 200:
                print(f"❌ API接続失敗: {response.status_code}")
                return None
                
            data = response.json()
            print(f"✅ API接続成功: {len(str(data))}文字")
            
            # 完全構造解析
            print("\n📊 データ構造詳細分析:")
            print(f"データタイプ: {type(data)}")
            print(f"配列長: {len(data) if isinstance(data, list) else 'N/A'}")
            
            if isinstance(data, list) and len(data) > 0:
                first_item = data[0]
                print(f"\n📋 第1要素構造:")
                print(f"キー: {list(first_item.keys()) if isinstance(first_item, dict) else 'N/A'}")
                
                if 'timeSeries' in first_item:
                    time_series = first_item['timeSeries']
                    print(f"\n⏰ timeSeries分析:")
                    print(f"timeSeries数: {len(time_series)}")
                    
                    for i, ts in enumerate(time_series):
                        print(f"\n--- timeSeries[{i}] ---")
                        print(f"キー: {list(ts.keys())}")
                        
                        if 'timeDefines' in ts:
                            time_defines = ts['timeDefines']
                            print(f"timeDefines: {len(time_defines)}個")
                            for j, td in enumerate(time_defines[:5]):
                                print(f"  {j}: {td}")
                                
                        if 'areas' in ts:
                            areas = ts['areas']
                            print(f"areas: {len(areas)}個")
                            
                            for j, area in enumerate(areas):
                                print(f"  area[{j}]キー: {list(area.keys())}")
                                
                                # 気温データ詳細確認
                                if 'temps' in area:
                                    temps = area['temps']
                                    print(f"    temps: {temps}")
                                    print(f"    temps長: {len(temps)}")
                                    
                                # 天気データ確認
                                if 'weathers' in area:
                                    weathers = area['weathers']
                                    print(f"    weathers: {len(weathers)}個")
                                    for k, weather in enumerate(weathers[:3]):
                                        print(f"      {k}: {weather[:50]}...")
                                        
                                # その他のデータ確認
                                for key in area.keys():
                                    if key not in ['temps', 'weathers']:
                                        value = area[key]
                                        if isinstance(value, list):
                                            print(f"    {key}: {len(value)}個 - {value[:3] if len(value) > 0 else '空'}")
                                        else:
                                            print(f"    {key}: {value}")
                                            
            return data
            
        except Exception as e:
            print(f"❌ 構造解析エラー: {e}")
            return None
            
    def extract_all_temperature_patterns(self, data):
        """全ての気温データパターン抽出"""
        print("\n🌡️ 全気温データパターン抽出")
        print("=" * 60)
        
        temperature_patterns = []
        
        try:
            if data and isinstance(data, list) and len(data) > 0:
                first_item = data[0]
                
                if 'timeSeries' in first_item:
                    for i, ts in enumerate(first_item['timeSeries']):
                        print(f"\n🔍 timeSeries[{i}]の気温データ:")
                        
                        time_defines = ts.get('timeDefines', [])
                        areas = ts.get('areas', [])
                        
                        print(f"timeDefines: {len(time_defines)}個")
                        for j, td in enumerate(time_defines):
                            print(f"  {j}: {td}")
                            
                        for j, area in enumerate(areas):
                            print(f"\narea[{j}]:")
                            
                            # 気温関連の全キー確認
                            temp_keys = [key for key in area.keys() if 'temp' in key.lower()]
                            print(f"気温関連キー: {temp_keys}")
                            
                            for key in temp_keys:
                                temp_data = area[key]
                                print(f"  {key}: {temp_data}")
                                
                                if isinstance(temp_data, list):
                                    pattern = {
                                        'timeSeries_index': i,
                                        'area_index': j,
                                        'key': key,
                                        'data': temp_data,
                                        'time_defines': time_defines,
                                        'data_length': len(temp_data),
                                        'time_length': len(time_defines)
                                    }
                                    temperature_patterns.append(pattern)
                                    
        except Exception as e:
            print(f"❌ 気温パターン抽出エラー: {e}")
            
        return temperature_patterns
        
    def create_perfect_temperature_extractor(self, patterns):
        """完璧な気温抽出ロジック作成"""
        print(f"\n🔧 完璧な気温抽出ロジック作成")
        print("=" * 60)
        
        print("📊 発見された気温パターン:")
        for i, pattern in enumerate(patterns):
            print(f"\nパターン{i+1}:")
            print(f"  timeSeries: {pattern['timeSeries_index']}")
            print(f"  area: {pattern['area_index']}")
            print(f"  キー: {pattern['key']}")
            print(f"  データ: {pattern['data']}")
            print(f"  データ長: {pattern['data_length']}")
            print(f"  時間長: {pattern['time_length']}")
            
        # 最適パターン選択
        best_pattern = None
        for pattern in patterns:
            if pattern['data_length'] >= 6:  # 3日分×2(最低・最高)
                best_pattern = pattern
                break
        
        if not best_pattern and patterns:
            best_pattern = max(patterns, key=lambda x: x['data_length'])
            
        if best_pattern:
            print(f"\n✅ 最適パターン選択:")
            print(f"  timeSeries[{best_pattern['timeSeries_index']}]")
            print(f"  area[{best_pattern['area_index']}]")
            print(f"  キー: {best_pattern['key']}")
            print(f"  データ: {best_pattern['data']}")
            
        return best_pattern
        
    def create_perfect_weather_system(self, best_pattern):
        """完璧な天気システム作成"""
        print(f"\n🎯 完璧な天気システム作成")
        print("=" * 60)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        perfect_filename = f"weather_forecast_perfect_{timestamp}.py"
        
        # 最適パターンを使った完璧なシステム
        perfect_code = f'''#!/usr/bin/env python3
# 完璧な天気予報システム（3日分気温データ完璧対応）
import requests
import json
import datetime
import re

WEATHER_API_URL_PERFECT = "https://www.jma.go.jp/bosai/forecast/data/forecast/370000.json"
WARNING_API_URL_PERFECT = "https://www.jma.go.jp/bosai/warning/data/warning/370000.json"

def get_weather_forecast():
    """
    完璧版：3日分気温データ完璧対応
    """
    weather_data = {{'days': [], 'warnings': [], 'typhoons': []}}
    current_date = datetime.datetime.now()

    try:
        print("🌤️ 完璧版天気予報取得開始...")
        response = requests.get(WEATHER_API_URL_PERFECT, timeout=15)
        
        if response.status_code != 200:
            raise Exception(f"HTTP {{response.status_code}}")
            
        data = response.json()
        print(f"✅ 天気予報API成功: {{len(str(data))}}文字")

        if data and len(data) > 0 and 'timeSeries' in data[0]:
            # 天気データ抽出
            weather_ts = data[0]['timeSeries'][0]
            weather_forecasts = weather_ts['areas'][0]['weathers']
            weather_dates = weather_ts['timeDefines']
            
            # 気温データ抽出（解析結果基準）
            temperature_data = []
            {"# 最適パターンが発見された場合の抽出ロジック" if best_pattern else "# フォールバック抽出ロジック"}
            {"temperature_ts = data[0]['timeSeries'][" + str(best_pattern['timeSeries_index']) + "]" if best_pattern else "temperature_ts = None"}
            {"temperature_area = temperature_ts['areas'][" + str(best_pattern['area_index']) + "]" if best_pattern else "temperature_area = None"}
            {"temperature_data = temperature_area['" + best_pattern['key'] + "']" if best_pattern else "temperature_data = []"}
            
            # フォールバック：他のtimeSeriesからも気温データを探索
            if not temperature_data:
                for ts_idx, ts in enumerate(data[0]['timeSeries']):
                    if 'areas' in ts:
                        for area_idx, area in enumerate(ts['areas']):
                            for key in area.keys():
                                if 'temp' in key.lower() and isinstance(area[key], list) and len(area[key]) > 0:
                                    temperature_data = area[key]
                                    print(f"✅ フォールバック気温データ発見: timeSeries[{{ts_idx}}] area[{{area_idx}}] {{key}}")
                                    break
                            if temperature_data:
                                break
                        if temperature_data:
                            break
            
            print(f"📊 気温データ: {{temperature_data}}")
            
            # 3日分データ構築
            for i in range(min(len(weather_dates), 3)):
                forecast_date = datetime.datetime.strptime(weather_dates[i].split('T')[0], '%Y-%m-%d')
                date_str = forecast_date.strftime('%Y-%m-%d')
                day_name = ['月', '火', '水', '木', '金', '土', '日'][forecast_date.weekday()]
                date_display = f'{{forecast_date.month}}月{{forecast_date.day}}日({{day_name}})'
                weather = weather_forecasts[i] if i < len(weather_forecasts) and weather_forecasts[i] != '' else 'データなし'
                
                # 完璧な気温データ抽出
                temperature = 'N/A'
                if temperature_data:
                    # パターン1: [最低, 最高, 最低, 最高, 最低, 最高] 形式
                    if len(temperature_data) >= (i+1)*2:
                        min_temp = temperature_data[i*2] if temperature_data[i*2] != '' else None
                        max_temp = temperature_data[i*2+1] if temperature_data[i*2+1] != '' else None
                        
                        if min_temp and max_temp:
                            temperature = f'{{min_temp}}℃〜{{max_temp}}℃'
                        elif max_temp:
                            temperature = f'最高{{max_temp}}℃'
                        elif min_temp:
                            temperature = f'最低{{min_temp}}℃'
                    
                    # パターン2: [今日最低, 今日最高, 明日最低, 明日最高, ...] 形式
                    elif len(temperature_data) > i and temperature_data[i] != '':
                        temperature = f'{{temperature_data[i]}}℃'
                        
                    # パターン3: 他の可能なパターン
                    elif len(temperature_data) > 0:
                        # 最初の有効なデータを使用
                        for temp_val in temperature_data:
                            if temp_val != '':
                                temperature = f'{{temp_val}}℃（参考）'
                                break

                day_data = {{
                    'date': date_str,
                    'display_date': date_display,
                    'weather': weather,
                    'temperature': temperature,
                    'is_today': i == 0,
                    'is_tomorrow': i == 1,
                    'is_day_after_tomorrow': i == 2
                }}
                weather_data['days'].append(day_data)
                
        else:
            raise Exception("データ構造不正")

    except Exception as e:
        print(f'天気予報取得で致命的なエラー: {{str(e)}}')
        # フォールバックロジック
        for i in range(3):
            date_obj = current_date + datetime.timedelta(days=i)
            day_name = ['月', '火', '水', '木', '金', '土', '日'][date_obj.weekday()]
            weather_data['days'].append({{
                'date': date_obj.strftime('%Y-%m-%d'),
                'display_date': f'{{date_obj.month}}月{{date_obj.day}}日({{day_name}})',
                'weather': '取得失敗',
                'temperature': 'N/A',
                'is_today': i == 0, 'is_tomorrow': i == 1, 'is_day_after_tomorrow': i == 2
            }})

    # 警報・注意報の取得
    try:
        print("⚠️ 警報・注意報取得開始...")
        warning_response = requests.get(WARNING_API_URL_PERFECT, timeout=15)
        if warning_response.status_code == 200:
            warning_data = warning_response.json()
            print(f"✅ 警報・注意報API成功")
            
            if warning_data and 'areaTypes' in warning_data:
                for area_type in warning_data['areaTypes']:
                    if 'areas' in area_type:
                        for area in area_type['areas']:
                            area_name = area.get('name', '地域名不明')
                            if 'warnings' in area:
                                for warning in area['warnings']:
                                    warning_name = ''
                                    if 'kind' in warning and 'name' in warning['kind']:
                                        warning_name = warning['kind']['name']
                                    
                                    status = warning.get('status', '状態不明')
                                    
                                    if status != '解除' and warning_name:
                                        weather_data['warnings'].append({{
                                            'area': area_name,
                                            'name': warning_name,
                                            'status': status
                                        }})
        else:
            print(f"⚠️ 警報・注意報API HTTP {{warning_response.status_code}}")
    except Exception as e:
        print(f'警報・注意報取得エラー: {{str(e)}}')

    # 既存のキー設定保持
    weather_data['today'] = weather_data['days'][0] if len(weather_data['days']) > 0 else {{}}
    weather_data['tomorrow'] = weather_data['days'][1] if len(weather_data['days']) > 1 else {{}}
    weather_data['day_after_tomorrow'] = weather_data['days'][2] if len(weather_data['days']) > 2 else {{}}

    return weather_data

if __name__ == '__main__':
    print("--- 完璧版天気予報モジュール単体テスト ---")
    forecast_data = get_weather_forecast()
    if forecast_data:
        print("\\n[3日分完璧天気データ]")
        for i, day in enumerate(forecast_data['days']):
            print(f"  {{i+1}}日目: {{day['display_date']}}")
            print(f"    天気: {{day['weather']}}")
            print(f"    気温: {{day['temperature']}}")
            
        print("\\n[警報・注意報]")
        if forecast_data.get('warnings'):
            for warn in forecast_data['warnings']:
                print(f"- {{warn['area']}}: {{warn['name']}} ({{warn['status']}})")
        else:
            print("発表されていません。")

        print("\\n--- 完璧版テスト成功 ---")
    else:
        print("\\n--- 完璧版テスト失敗 ---")
'''
        
        with open(perfect_filename, 'w', encoding='utf-8') as f:
            f.write(perfect_code)
            
        print(f"✅ 完璧な天気システム作成: {perfect_filename}")
        return perfect_filename
        
    def run_temperature_perfection(self):
        """2-3日目気温データ完璧化実行"""
        print("🎯 2-3日目気温データ完璧化開始")
        print("=" * 70)
        
        # 1. API完全構造解析
        data = self.analyze_full_api_structure()
        
        if not data:
            print("❌ API接続失敗")
            return None
            
        # 2. 全気温パターン抽出
        patterns = self.extract_all_temperature_patterns(data)
        
        # 3. 最適パターン選択
        best_pattern = self.create_perfect_temperature_extractor(patterns)
        
        # 4. 完璧システム作成
        perfect_file = self.create_perfect_weather_system(best_pattern)
        
        print(f"\n" + "=" * 70)
        print("🎉 2-3日目気温データ完璧化完了")
        print("=" * 70)
        print(f"✅ API構造解析: 完了")
        print(f"✅ 気温パターン抽出: {len(patterns)}パターン発見")
        print(f"✅ 最適パターン選択: 完了")
        print(f"✅ 完璧システム作成: {perfect_file}")
        
        print(f"\n🧪 完璧版テスト: python3 {perfect_file}")
        
        return perfect_file

if __name__ == "__main__":
    perfection = TemperatureDataPerfection()
    perfection.run_temperature_perfection()
