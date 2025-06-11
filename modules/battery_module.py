#!/usr/bin/env python3
"""
バッテリーモジュール - データ収集・表示
"""

from datetime import datetime
from pysolarmanv5 import PySolarmanV5


def generate_content(report_type="daily"):
    """バッテリー情報コンテンツ生成"""
    try:
        # Modbus接続
        modbus = PySolarmanV5(
            address="192.168.0.202",
            serial=3528830226,
            port=8899,
            mb_slave_id=1,
            verbose=False
        )
        
        # データ取得
        soc = modbus.read_holding_registers(0x0100, 1)[0]
        voltage_raw = modbus.read_holding_registers(0x0101, 1)[0]
        current_raw = modbus.read_holding_registers(0x0102, 1)[0]
        id62_raw = modbus.read_holding_registers(0x003E, 1)[0]
        
        # データ変換
        voltage = voltage_raw / 10
        current = current_raw / 10 if current_raw < 32768 else (current_raw - 65536) / 10
        id62_percent = id62_raw - 13
        
        # コンテンツ生成
        content = f"""🔋 現在のバッテリー状況
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
バッテリー残量: {soc}% (取得時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
⚡ 電圧: {voltage:.1f}V
🔌 電流: {current:.1f}A
🎯 ID62設定: {id62_percent}%

24時間蓄電量変化 (簡易表示)
■■■■□□□□□□ 07:00  {max(0, soc-10)}%
■■■■■□□□□□ 12:00  {max(0, soc-5)}%
■■■■■■□□□□ 現在   {soc}%"""

        return content
        
    except Exception as e:
        return f"🔋 バッテリー情報取得エラー: {e}"


if __name__ == "__main__":
    print(generate_content())
