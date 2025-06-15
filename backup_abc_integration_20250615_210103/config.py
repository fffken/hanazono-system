import json
import os
import logging

SETTINGS_FILE = 'settings.json'

def get_settings():
    """
    設定ファイルを読み込み、環境変数を展開して返す。
    失敗した場合は例外を発生させる。
    """
    logger = logging.getLogger(__name__)
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            settings_data = json.load(f)
        
        # 環境変数を再帰的に展開
        def expand_vars(config):
            if isinstance(config, dict):
                return {k: expand_vars(v) for k, v in config.items()}
            elif isinstance(config, list):
                return [expand_vars(i) for i in config]
            elif isinstance(config, str):
                return os.path.expandvars(config)
            return config

        return expand_vars(settings_data)

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"FATAL: {SETTINGS_FILE} の読み込みまたは解析に失敗しました: {e}")
        raise

# 天気予報API設定
WEATHER_API_URL = "http://weather.livedoor.com/forecast/webservice/json/v1"
WARNING_API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/"
TYPHOON_API_URL = "https://www.jma.go.jp/bosai/typhoon/data/typhoon/"

# 天気予報地域コード（香川県高松市）
WEATHER_AREA_CODE = "370000"

# フォールバック天気データ
FALLBACK_WEATHER = {
    "today": {"weather": "晴れ", "temperature": {"max": "25", "min": "15"}},
    "tomorrow": {"weather": "曇り", "temperature": {"max": "23", "min": "14"}},
    "day_after_tomorrow": {"weather": "雨", "temperature": {"max": "20", "min": "12"}}
}
