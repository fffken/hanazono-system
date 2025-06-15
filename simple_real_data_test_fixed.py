#!/usr/bin/env python3
# シンプル実データメールテスト（電圧小数点1桁修正版）
import glob
import json
import os

def get_real_battery_data():
    try:
        json_files = glob.glob('data/collected_data_*.json')
        if not json_files:
            return None
        latest_file = max(json_files, key=lambda x: os.path.getctime(x))
        with open(latest_file, 'r') as f:
            data = json.load(f)
        record = data[0] if isinstance(data, list) else data
        params = record.get('parameters', {})
        soc = params.get('0x0100', {}).get('value', 'N/A')
        voltage_raw = params.get('0x0101', {}).get('value', 'N/A')
        
        # 電圧を小数点1桁に丸め
        if voltage_raw != 'N/A':
            voltage = round(float(voltage_raw), 1)
        else:
            voltage = 'N/A'
            
        timestamp = record.get('datetime', 'N/A')
        return {'soc': soc, 'voltage': voltage, 'timestamp': timestamp}
    except:
        return None

print("🧪 実データ取得テスト（電圧修正版）")
data = get_real_battery_data()
print(f"SOC: {data['soc']}%, 電圧: {data['voltage']}V, 時刻: {data['timestamp']}")
