def get_real_battery_data():
    """実際のバッテリーデータ取得"""
    import json
    import glob
    import os
    
    try:
        # 最新データファイル取得
        json_files = glob.glob('data/collected_data_*.json')
        if not json_files:
            return None
            
        latest_file = max(json_files, key=os.path.getctime)
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 最新レコード取得
        latest_record = data[0] if isinstance(data, list) else data
        params = latest_record.get('parameters', {})
        
        # バッテリーデータ抽出
        battery_info = {}
        
        # SOC
        if '0x0100' in params:
            soc = params['0x0100']
            battery_info['soc'] = soc.get('value', soc.get('raw_value', 0))
            
        # 電圧
        if '0x0101' in params:
            voltage = params['0x0101']
            battery_info['voltage'] = voltage.get('value', voltage.get('raw_value', 0))
            
        # 電流
        if '0x0102' in params:
            current = params['0x0102']
            battery_info['current'] = current.get('value', current.get('raw_value', 0))
            
        battery_info['timestamp'] = latest_record.get('datetime', 'Unknown')
        
        return battery_info
        
    except Exception as e:
        print(f"バッテリーデータ取得エラー: {e}")
        return None

# テスト実行
if __name__ == "__main__":
    data = get_real_battery_data()
    if data:
        print("✅ 実データ取得テスト成功:")
        print(f"   SOC: {data.get('soc', 'N/A')}%")
        print(f"   電圧: {data.get('voltage', 'N/A')}V") 
        print(f"   電流: {data.get('current', 'N/A')}A")
        print(f"   時刻: {data.get('timestamp', 'N/A')}")
    else:
        print("❌ 実データ取得失敗")