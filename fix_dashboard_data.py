import json
from pathlib import Path

def test_data_loading():
    """データ読み込みテスト"""
    try:
        data_dir = Path('/home/pi/lvyuan_solar_control/data')
        files = list(data_dir.glob('lvyuan_data_*.json'))
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        with open(latest_file) as f:
            data = json.load(f)
        
        if isinstance(data, list) and len(data) > 0 and data[0]:
            print('✅ データ構造正常')
            return data[0]
        else:
            print('❌ データ構造異常')
            return None
    except Exception as e:
        print(f'エラー: {e}')
        return None

if __name__ == '__main__':
    result = test_data_loading()
    if result and 'parameters' in result:
        print('✅ parametersキー存在')
    else:
        print('❌ parametersキーなし')
