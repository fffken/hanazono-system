from settings_manager import SettingsManager

def main():
    """簡易設定確認ツール"""
    settings = SettingsManager()
    print('\n===== ソーラー蓄電システム 設定確認 =====')
    print('\n■季節別設定:')
    for season, types in settings._settings.get('seasonal_settings', {}).items():
        print(f'\n{season}:')
        for type_name, values in types.items():
            print(f'  - {type_name}: {values}')
    print('\n■インバーターパラメータ:')
    for key, value in settings._settings.get('inverter_parameters', {}).items():
        print(f'  - {key}: {value}')
    print('\n■天気アイコン数:', len(settings._settings.get('weather_icons', {})))
    print('■季節アイコン数:', len(settings._settings.get('season_icons', {})))
    print('\n■メール通知:', '有効' if settings.is_email_enabled() else '無効')
    print('■LINE通知:', '有効' if settings.is_line_enabled() else '無効')
    print('\n設定の表示が完了しました。終了するにはEnterキーを押してください。')
    input()
if __name__ == '__main__':
    main()