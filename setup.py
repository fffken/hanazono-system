"""LVYUANソーラー蓄電システム自動最適化セットアップ"""
import os
import sys
import json
import subprocess
import getpass

def print_header(text):
    """ヘッダー表示"""
    print('\n' + '=' * 60)
    print(f' {text} '.center(60, '='))
    print('=' * 60 + '\n')

def get_input(prompt, default=None):
    """ユーザー入力取得"""
    default_text = f' [{default}]' if default is not None else ''
    value = input(f'{prompt}{default_text}: ') or default
    return value

def setup_settings():
    """設定ファイルのセットアップ"""
    print_header('設定ファイルのセットアップ')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file = os.path.join(script_dir, 'settings.json')
    settings = {}
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r') as f:
                settings = json.load(f)
            print('既存の設定ファイルを読み込みました')
        except Exception as e:
            print(f'既存の設定ファイルの読み込みに失敗しました: {e}')
    if 'inverter' not in settings:
        settings['inverter'] = {}
    print('\n== インバーター設定 ==')
    settings['inverter']['ip'] = get_input('インバーターのIPアドレス', settings['inverter'].get('ip', '192.168.0.202'))
    settings['inverter']['serial'] = int(get_input('インバーターのシリアル番号', settings['inverter'].get('serial', '3528830226')))
    settings['inverter']['mac'] = get_input('インバーターのMACアドレス', settings['inverter'].get('mac', 'D4:27:87:16:7A:F8'))
    settings['inverter']['port'] = int(get_input('インバーターのポート番号', settings['inverter'].get('port', '8899')))
    settings['inverter']['mb_slave_id'] = int(get_input('ModbusスレーブID', settings['inverter'].get('mb_slave_id', '1')))
    if 'network' not in settings:
        settings['network'] = {}
    print('\n== ネットワーク設定 ==')
    settings['network']['subnet'] = get_input('ネットワークサブネット', settings['network'].get('subnet', '192.168.0.0/24'))
    if 'email' not in settings:
        settings['email'] = {}
    print('\n== メール設定 ==')
    settings['email']['smtp_server'] = get_input('SMTPサーバー', settings['email'].get('smtp_server', ''))
    settings['email']['smtp_port'] = int(get_input('SMTPポート', settings['email'].get('smtp_port', '587')))
    settings['email']['smtp_user'] = get_input('SMTPユーザー名', settings['email'].get('smtp_user', ''))
    settings['email']['smtp_password'] = get_input('SMTPパスワード', settings['email'].get('smtp_password', ''))
    settings['email']['sender'] = get_input('送信者メールアドレス', settings['email'].get('sender', ''))
    recipients = settings['email'].get('recipients', [])
    if recipients:
        print(f"現在の受信者: {', '.join(recipients)}")
        change = input('受信者リストを変更しますか？ (y/N): ').lower() == 'y'
    else:
        change = True
    if change:
        settings['email']['recipients'] = []
        while True:
            recipient = input('受信者メールアドレス (空白で終了): ')
            if not recipient:
                break
            settings['email']['recipients'].append(recipient)
    if 'monitoring' not in settings:
        settings['monitoring'] = {}
    print('\n== 監視設定 ==')
    settings['monitoring']['interval_minutes'] = int(get_input('データ収集間隔 (分)', settings['monitoring'].get('interval_minutes', '15')))
    try:
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
        print('\n設定ファイルを保存しました')
    except Exception as e:
        print(f'\n設定ファイルの保存に失敗しました: {e}')
        return False
    return True

def install_dependencies():
    """依存パッケージのインストール"""
    print_header('依存パッケージのインストール')
    packages = ['pysolarmanv5', 'matplotlib', 'numpy']
    try:
        for package in packages:
            print(f'パッケージ {package} をインストールしています...')
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
        print('\nすべてのパッケージがインストールされました')
        return True
    except subprocess.CalledProcessError as e:
        print(f'\nパッケージインストールエラー: {e}')
        return False
    except Exception as e:
        print(f'\n予期しないエラー: {e}')
        return False

def setup_cron():
    """cronジョブのセットアップ"""
    print_header('cronジョブのセットアップ')
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.join(script_dir, 'main.py')
        os.chmod(main_script, 493)
        result = subprocess.run([sys.executable, main_script, '--setup'], check=True)
        print('\ncronジョブの設定に成功しました')
        return True
    except subprocess.CalledProcessError as e:
        print(f'\ncronジョブ設定エラー: {e}')
        return False
    except Exception as e:
        print(f'\n予期しないエラー: {e}')
        return False

def run_test():
    """動作テスト実行"""
    print_header('動作テスト')
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.join(script_dir, 'main.py')
        print('データ収集テストを実行しています...')
        subprocess.run([sys.executable, main_script, '--collect', '--debug'], check=True)
        print('\nテストが成功しました')
        return True
    except subprocess.CalledProcessError as e:
        print(f'\nテストエラー: {e}')
        return False
    except Exception as e:
        print(f'\n予期しないエラー: {e}')
        return False

def main():
    """メイン処理"""
    print_header('LVYUANソーラー蓄電システム自動最適化セットアップ')
    steps = [('依存パッケージのインストール', install_dependencies), ('設定ファイルの作成', setup_settings), ('cronジョブの設定', setup_cron), ('動作テスト', run_test)]
    results = {}
    for name, func in steps:
        print(f'\n[ステップ] {name}')
        proceed = input('実行しますか？ (Y/n): ').lower() != 'n'
        if proceed:
            success = func()
            results[name] = '成功' if success else '失敗'
        else:
            results[name] = 'スキップ'
    print_header('セットアップ結果')
    for name, result in results.items():
        print(f'{name}: {result}')
    if all((result == '成功' or result == 'スキップ' for result in results.values())):
        print('\nセットアップが正常に完了しました！')
        print('次のコマンドでシステムを実行できます:')
        print('  python main.py --collect  # データ収集')
        print('  python main.py --daily-report  # 日次レポート送信')
    else:
        print('\n一部のセットアップが失敗しました。エラーを確認して再試行してください。')
if __name__ == '__main__':
    main()