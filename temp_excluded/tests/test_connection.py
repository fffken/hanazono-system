import sys
import time
from pysolarmanv5 import PySolarmanV5

def test_connection(ip, serial_number):
    print(f'IPアドレス {ip}, シリアル番号 {serial_number} で接続テスト中...')
    try:
        modbus = PySolarmanV5(address=ip, serial=serial_number, port=8899, mb_slave_id=1, verbose=True)
        print('接続成功！テストレジスタ読み取り中...')
        register_ranges = [(0, 10, 'システム設定'), (57344, 10, '拡張設定'), (256, 10, '計測値'), (28672, 10, 'ステータス')]
        for start_addr, count, description in register_ranges:
            print(f'\n{description}レジスタ ({hex(start_addr)}～{hex(start_addr + count - 1)}) 読み取り試行...')
            try:
                values = modbus.read_holding_registers(start_addr, count)
                print(f'読み取り成功: {values}')
                for i, value in enumerate(values):
                    if value != 0:
                        print(f'  レジスタ {hex(start_addr + i)}: {value}')
                print(f'レジスタ範囲 {hex(start_addr)}～{hex(start_addr + count - 1)} の読み取り成功')
            except Exception as e:
                print(f'読み取りエラー: {e}')
            time.sleep(1)
        print('\n接続テスト完了')
    except Exception as e:
        print(f'接続エラー: {e}')
        import traceback
        traceback.print_exc()
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'使用法: {sys.argv[0]} <IPアドレス> <シリアル番号>')
        sys.exit(1)
    ip = sys.argv[1]
    serial_number = int(sys.argv[2])
    test_connection(ip, serial_number)