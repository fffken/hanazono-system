import sys
import time
from pysolarmanv5 import PySolarmanV5

def read_register(ip, serial, register):
    """レジスタの値を読み取る"""
    try:
        modbus = PySolarmanV5(address=ip, serial=serial, port=8899, mb_slave_id=1, verbose=False)
        return modbus.read_holding_registers(register, 1)[0]
    except Exception as e:
        print(f'読み取りエラー: {e}')
        return None

def write_register(ip, serial, register, value):
    """レジスタに値を書き込む"""
    try:
        modbus = PySolarmanV5(address=ip, serial=serial, port=8899, mb_slave_id=1, verbose=False)
        modbus.write_holding_register(register, value)
        return True
    except Exception as e:
        print(f'書き込みエラー: {e}')
        return False

def main():
    if len(sys.argv) < 5:
        print(f'使用法: {sys.argv[0]} <IPアドレス> <シリアル番号> <レジスタアドレス(16進数)> <新しい値>')
        sys.exit(1)
    ip = sys.argv[1]
    serial = int(sys.argv[2])
    register = int(sys.argv[3], 16)
    new_value = int(sys.argv[4])
    print(f'\nレジスタ {hex(register)} の書き込みテスト')
    current_value = read_register(ip, serial, register)
    if current_value is None:
        print('現在値の読み取りに失敗しました')
        sys.exit(1)
    print(f'現在の値: {current_value}')
    time.sleep(1)
    print(f'新しい値 {new_value} を書き込み中...')
    if not write_register(ip, serial, register, new_value):
        print('書き込みに失敗しました')
        sys.exit(1)
    print('書き込み完了')
    print('5秒待機...')
    time.sleep(5)
    updated_value = read_register(ip, serial, register)
    if updated_value is None:
        print('更新後の値の読み取りに失敗しました')
        sys.exit(1)
    print(f'更新後の値: {updated_value}')
    if updated_value == new_value:
        print('✓ 書き込みテスト成功')
    else:
        print('✗ 書き込みテスト失敗 - 値が変更されませんでした')
    choice = input('\n元の値 (' + str(current_value) + ') に戻しますか？ (y/n): ')
    if choice.lower() == 'y':
        print(f'元の値 {current_value} に戻します...')
        if write_register(ip, serial, register, current_value):
            print('元の値に戻しました')
            time.sleep(2)
            restored_value = read_register(ip, serial, register)
            if restored_value is not None:
                print(f'復元後の値: {restored_value}')
        else:
            print('元の値への復元に失敗しました')
if __name__ == '__main__':
    main()