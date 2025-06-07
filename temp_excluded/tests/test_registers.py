import sys
import time
from pysolarmanv5 import PySolarmanV5

def read_register(ip, serial, register, description):
    print(f'\nレジスタ {hex(register)} ({description}) を読み取り中...')
    try:
        modbus = PySolarmanV5(address=ip, serial=serial, port=8899, mb_slave_id=1, verbose=False)
        value = modbus.read_holding_registers(register, 1)[0]
        print(f'成功: {value}')
        return value
    except Exception as e:
        print(f'エラー: {e}')
        return None

def main():
    if len(sys.argv) != 3:
        print(f'使用法: {sys.argv[0]} <IPアドレス> <シリアル番号>')
        sys.exit(1)
    ip = sys.argv[1]
    serial = int(sys.argv[2])
    registers_to_test = [(57345, 'PV充電電流設定'), (57346, '充電電流(レジスタ)'), (57347, '充電時間(レジスタ)'), (57349, 'SOC設定(レジスタ)'), (57359, '充電・放電カットオフSOC'), (57361, '均等充電時間'), (57362, 'ブースト充電時間'), (57866, '最大充電電流')]
    for register, desc in registers_to_test:
        read_register(ip, serial, register, desc)
        time.sleep(3)
if __name__ == '__main__':
    main()