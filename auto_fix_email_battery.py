#!/usr/bin/env python3
"""AI自動問題解決：メールのバッテリー情報修正"""
import re

# 問題：report_dataの構造でバッテリー情報抽出失敗
# 解決：enhanced_email_system_v2.pyの_extract_battery_info修正

with open('enhanced_email_system_v2.py', 'r') as f:
    content = f.read()

# data['solar_data']からparametersを取得するよう修正
old_pattern = r'if isinstance\(data, list\) and len\(data\) > 0:\s*actual_data = data\[0\]'
new_pattern = '''if isinstance(data, dict) and 'solar_data' in data:
            # report_data形式の場合
            solar_data = data['solar_data']
            if isinstance(solar_data, list) and len(solar_data) > 0:
                actual_data = solar_data[0]
            else:
                actual_data = solar_data
        elif isinstance(data, list) and len(data) > 0:
            actual_data = data[0]'''

content = re.sub(old_pattern, new_pattern, content, flags=re.DOTALL)

with open('enhanced_email_system_v2.py', 'w') as f:
    f.write(content)

print("✅ AI自動修正完了：メールバッテリー情報抽出修正")
