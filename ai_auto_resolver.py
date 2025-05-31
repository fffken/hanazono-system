#!/usr/bin/env python3
"""
次世代AI自動問題解決システム v1.0
GitHub連携・自動修正・テスト・復旧機能統合
"""
import os
import subprocess
import json
import shutil
from datetime import datetime

class AIAutoResolver:
    def __init__(self):
        self.base_dir = "/home/pi/lvyuan_solar_control"
        self.backup_dir = f"{self.base_dir}/ai_backups"
        os.makedirs(self.backup_dir, exist_ok=True)
        
    def solve_email_battery_issue(self):
        """メールバッテリー情報問題の完全自動解決"""
        print("🤖 AI自動問題解決開始：メールバッテリー情報修正")
        
        # Step 1: 自動バックアップ
        backup_file = self._create_backup('enhanced_email_system_v2.py')
        print(f"💾 自動バックアップ: {backup_file}")
        
        # Step 2: 安全な修正実行
        if self._fix_battery_extraction():
            # Step 3: 自動構文チェック
            if self._syntax_check('enhanced_email_system_v2.py'):
                # Step 4: 自動テスト
                if self._test_email_system():
                    print("✅ 完全自動解決成功！")
                    return True
                else:
                    print("❌ テスト失敗 - 自動復旧中...")
            else:
                print("❌ 構文エラー - 自動復旧中...")
        
        # Step 5: 自動復旧
        self._restore_from_backup(backup_file)
        print("🔄 自動復旧完了")
        return False
    
    def _create_backup(self, filename):
        """自動バックアップ作成"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{self.backup_dir}/{filename}.backup_{timestamp}"
        shutil.copy(f"{self.base_dir}/{filename}", backup_path)
        return backup_path
    
    def _fix_battery_extraction(self):
        """バッテリー抽出処理修正"""
        try:
            file_path = f"{self.base_dir}/enhanced_email_system_v2.py"
            with open(file_path, 'r') as f:
                content = f.read()
            
            # 安全な修正：既存の関数を完全に置き換え
            new_function = '''    def _extract_battery_info(self, data):
        """バッテリー情報を抽出（report_data形式対応版）"""
        try:
            # report_data形式の場合
            if isinstance(data, dict) and 'solar_data' in data:
                solar_data = data['solar_data']
                if isinstance(solar_data, list) and len(solar_data) > 0:
                    actual_data = solar_data[0]
                else:
                    actual_data = solar_data
            elif isinstance(data, list) and len(data) > 0:
                actual_data = data[0]
            elif isinstance(data, dict):
                actual_data = data
            else:
                return {'soc': 'N/A', 'voltage': 'N/A', 'current': 'N/A'}
            
            if isinstance(actual_data, dict) and 'parameters' in actual_data:
                params = actual_data['parameters']
                soc = 'N/A'
                voltage = 'N/A'
                current = 'N/A'
                
                if '0x0100' in params and isinstance(params['0x0100'], dict):
                    soc = params['0x0100'].get('value', 'N/A')
                if '0x0101' in params and isinstance(params['0x0101'], dict):
                    voltage_val = params['0x0101'].get('value', 'N/A')
                    voltage = round(voltage_val, 1) if isinstance(voltage_val, (int, float)) else 'N/A'
                if '0x0102' in params and isinstance(params['0x0102'], dict):
                    current_val = params['0x0102'].get('value', 'N/A')
                    current = round(current_val, 1) if isinstance(current_val, (int, float)) else 'N/A'
                
                return {'soc': soc, 'voltage': voltage, 'current': current}
            else:
                return {'soc': 'N/A', 'voltage': 'N/A', 'current': 'N/A'}
        except Exception as e:
            return {'soc': 'N/A', 'voltage': 'N/A', 'current': 'N/A'}'''
            
            # 既存の関数を置き換え
            import re
            pattern = r'def _extract_battery_info\(self, data\):.*?(?=\n    def |\nclass |\Z)'
            content = re.sub(pattern, new_function, content, flags=re.DOTALL)
            
            with open(file_path, 'w') as f:
                f.write(content)
            
            return True
        except Exception as e:
            print(f"修正エラー: {e}")
            return False
    
    def _syntax_check(self, filename):
        """自動構文チェック"""
        try:
            result = subprocess.run(['python3', '-m', 'py_compile', filename], 
                                  cwd=self.base_dir, capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def _test_email_system(self):
        """メールシステム自動テスト"""
        try:
            # インポートテスト
            test_code = '''
import sys
sys.path.append("/home/pi/lvyuan_solar_control")
from enhanced_email_system_v2 import EnhancedEmailSystem
import json

# テストデータ
test_data = {
    "solar_data": [{
        "parameters": {
            "0x0100": {"value": 85, "name": "バッテリーSOC"},
            "0x0101": {"value": 53.5, "name": "バッテリー電圧"},
            "0x0102": {"value": 6.5, "name": "バッテリー電流"}
        }
    }]
}

# テスト実行
system = EnhancedEmailSystem(None, None)
result = system._extract_battery_info(test_data)
print("テスト結果:", result)

# 期待値チェック
if result["soc"] == 85 and result["voltage"] == 53.5:
    print("✅ テスト成功")
    exit(0)
else:
    print("❌ テスト失敗")
    exit(1)
'''
            result = subprocess.run(['python3', '-c', test_code], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def _restore_from_backup(self, backup_path):
        """自動復旧"""
        try:
            shutil.copy(backup_path, f"{self.base_dir}/enhanced_email_system_v2.py")
            return True
        except:
            return False

if __name__ == "__main__":
    resolver = AIAutoResolver()
    resolver.solve_email_battery_issue()
