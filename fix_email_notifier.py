import re

# email_notifier.pyを読み込み
with open('email_notifier.py', 'r') as f:
    content = f.read()

# 完全な電力情報セクションを置換
pattern = r'(        # 電力情報\n        report \+= "■ 電力情報\\n".*?)(?=        report \+= "\n")'
replacement = '''        # 電力情報
        report += "■ 電力情報\\n"
        if 'solar_data' in data and data['solar_data']:
            solar_data = data['solar_data']
            if isinstance(solar_data, list) and len(solar_data) > 0:
                latest_data = solar_data[0]
                if latest_data and 'parameters' in latest_data:
                    params = latest_data['parameters']
                    if '0x0100' in params:
                        battery_soc = params['0x0100']['value']
                        report += f"バッテリー残量: {battery_soc}%\\n"
                    if '0x0101' in params:
                        battery_voltage = params['0x0101']['value']
                        report += f"バッテリー電圧: {battery_voltage}V\\n"
                    if '0x0102' in params:
                        battery_current = params['0x0102']['value']
                        report += f"バッテリー電流: {battery_current}A\\n"
                else:
                    report += "データなし\\n"
            else:
                report += "データなし\\n"
        else:
            report += "データなし\\n"'''

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# ファイルに書き戻し
with open('email_notifier.py', 'w') as f:
    f.write(content)

print('✅ 電力情報セクションを完全に修正しました')
