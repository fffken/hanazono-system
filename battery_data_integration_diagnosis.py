#!/usr/bin/env python3
# バッテリーデータ統合診断・修復スクリプト
import os
import json
import glob
import datetime

class BatteryDataIntegrationFix:
    """CollectorCapsuleデータ→メール統合修復"""
    
    def __init__(self):
        self.latest_data = None
        self.integration_status = {}
        
    def diagnose_data_files(self):
        """データファイル診断"""
        print("🔍 バッテリーデータファイル診断")
        print("=" * 50)
        
        # 1. 最新JSONファイル確認
        json_files = glob.glob('data/collected_data_*.json')
        if json_files:
            latest_file = max(json_files, key=os.path.getctime)
            print(f"✅ 最新データファイル: {latest_file}")
            
            # ファイル内容確認
            try:
                with open(latest_file, 'r', encoding='utf-8') as f:
                    self.latest_data = json.load(f)
                    
                print(f"✅ JSONデータ読み込み成功")
                print(f"📊 データ構造確認:")
                
                if isinstance(self.latest_data, list) and len(self.latest_data) > 0:
                    sample = self.latest_data[0]
                    print(f"   - タイムスタンプ: {sample.get('datetime', 'N/A')}")
                    print(f"   - IPアドレス: {sample.get('ip_address', 'N/A')}")
                    
                    # パラメーター詳細確認
                    params = sample.get('parameters', {})
                    if params:
                        print(f"   - パラメーター数: {len(params)}")
                        for key, value in params.items():
                            name = value.get('name', 'Unknown')
                            val = value.get('value', value.get('raw_value', 'N/A'))
                            unit = value.get('unit', '')
                            print(f"     {key}: {name} = {val}{unit}")
                            
                    return True
                    
            except Exception as e:
                print(f"❌ JSONデータ読み込み失敗: {e}")
                return False
        else:
            print("❌ データファイル未発見")
            return False
            
    def extract_battery_data(self):
        """バッテリーデータ抽出"""
        print("\n🔋 バッテリーデータ抽出")
        print("=" * 50)
        
        if not self.latest_data:
            print("❌ データなし")
            return None
            
        try:
            # 最新データから主要パラメーター抽出
            latest_record = self.latest_data[0] if isinstance(self.latest_data, list) else self.latest_data
            params = latest_record.get('parameters', {})
            
            battery_data = {}
            
            # SOC (State of Charge)
            if '0x0100' in params:
                soc_data = params['0x0100']
                battery_data['soc'] = {
                    'value': soc_data.get('value', soc_data.get('raw_value')),
                    'unit': soc_data.get('unit', '%'),
                    'name': soc_data.get('name', 'バッテリーSOC')
                }
                
            # バッテリー電圧
            if '0x0101' in params:
                voltage_data = params['0x0101']
                battery_data['voltage'] = {
                    'value': voltage_data.get('value', voltage_data.get('raw_value')),
                    'unit': voltage_data.get('unit', 'V'),
                    'name': voltage_data.get('name', 'バッテリー電圧')
                }
                
            # バッテリー電流（あれば）
            if '0x0102' in params:
                current_data = params['0x0102']
                battery_data['current'] = {
                    'value': current_data.get('value', current_data.get('raw_value')),
                    'unit': current_data.get('unit', 'A'),
                    'name': current_data.get('name', 'バッテリー電流')
                }
                
            # タイムスタンプ
            battery_data['timestamp'] = latest_record.get('datetime', 'Unknown')
            battery_data['ip_address'] = latest_record.get('ip_address', 'Unknown')
            
            print("✅ バッテリーデータ抽出成功:")
            for key, value in battery_data.items():
                if isinstance(value, dict) and 'value' in value:
                    print(f"   {value['name']}: {value['value']}{value['unit']}")
                else:
                    print(f"   {key}: {value}")
                    
            return battery_data
            
        except Exception as e:
            print(f"❌ バッテリーデータ抽出失敗: {e}")
            return None
            
    def create_email_integration_code(self, battery_data):
        """メール統合コード生成"""
        print("\n📧 メール統合コード生成")
        print("=" * 50)
        
        if not battery_data:
            print("❌ バッテリーデータなし")
            return None
            
        # メール統合用の関数コード生成
        integration_code = f'''
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
        params = latest_record.get('parameters', {{}})
        
        # バッテリーデータ抽出
        battery_info = {{}}
        
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
        print(f"バッテリーデータ取得エラー: {{e}}")
        return None

# テスト実行
if __name__ == "__main__":
    data = get_real_battery_data()
    if data:
        print("✅ 実データ取得テスト成功:")
        print(f"   SOC: {{data.get('soc', 'N/A')}}%")
        print(f"   電圧: {{data.get('voltage', 'N/A')}}V") 
        print(f"   電流: {{data.get('current', 'N/A')}}A")
        print(f"   時刻: {{data.get('timestamp', 'N/A')}}")
    else:
        print("❌ 実データ取得失敗")
'''
        
        # テスト用ファイル保存
        test_file = f"battery_data_integration_test_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(integration_code.strip())
            
        print(f"✅ 統合コード生成: {test_file}")
        return test_file
        
    def run_complete_diagnosis(self):
        """完全診断実行"""
        print("🎯 バッテリーデータ統合診断開始")
        print("=" * 60)
        
        # 1. データファイル診断
        data_ok = self.diagnose_data_files()
        
        # 2. バッテリーデータ抽出
        battery_data = self.extract_battery_data()
        
        # 3. 統合コード生成
        integration_file = self.create_email_integration_code(battery_data)
        
        print(f"\n" + "=" * 60)
        print("📋 診断結果サマリー")
        print("=" * 60)
        print(f"✅ データファイル: {'OK' if data_ok else 'NG'}")
        print(f"✅ バッテリーデータ: {'OK' if battery_data else 'NG'}")
        print(f"✅ 統合コード: {'OK' if integration_file else 'NG'}")
        
        if data_ok and battery_data and integration_file:
            print(f"\n🎉 診断完了 - 統合準備OK")
            print(f"📁 統合テストファイル: {integration_file}")
            print(f"\n🚀 次のステップ:")
            print(f"   1. python3 {integration_file}  # 統合テスト")
            print(f"   2. メールシステムに統合コード適用")
        else:
            print(f"\n❌ 問題あり - 修復が必要")
            
        return data_ok, battery_data, integration_file

if __name__ == "__main__":
    fixer = BatteryDataIntegrationFix()
    fixer.run_complete_diagnosis()
