#!/usr/bin/env python3

import sys
import time
from pysolarmanv5 import PySolarmanV5

def read_register(ip, serial, register, description):
    print(f"\nレジスタ {hex(register)} ({description}) を読み取り中...")
    
    try:
        modbus = PySolarmanV5(
            address=ip,
            serial=serial,
            port=8899,
            mb_slave_id=1,
            verbose=False
        )
        
        value = modbus.read_holding_registers(register, 1)[0]
        print(f"成功: {value}")
        return value
    except Exception as e:
        print(f"エラー: {e}")
        return None

def main():
    if len(sys.argv) != 3:
        print(f"使用法: {sys.argv[0]} <IPアドレス> <シリアル番号>")
        sys.exit(1)
    
    ip = sys.argv[1]
    serial = int(sys.argv[2])
    
    # テスト対象の重要なレジスタ
    registers_to_test = [
        (0xE001, "PV充電電流設定"),
        (0xE002, "充電電流(レジスタ)"),
        (0xE003, "充電時間(レジスタ)"), 
        (0xE005, "SOC設定(レジスタ)"),
        (0xE00F, "充電・放電カットオフSOC"),
        (0xE011, "均等充電時間"),
        (0xE012, "ブースト充電時間"),
        (0xE20A, "最大充電電流")
    ]
    
    for register, desc in registers_to_test:
        read_register(ip, serial, register, desc)
        time.sleep(3)  # 3秒待機して接続負荷を軽減

if __name__ == "__main__":
    main()
