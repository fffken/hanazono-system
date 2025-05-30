from settings_manager import SettingsManager
from season_detector import get_detailed_season

class SettingsRecommender:
    """天気と季節に基づいて設定を推奨するクラス"""

    def __init__(self):
        """初期化"""
        self.settings_manager = SettingsManager()

    def recommend_settings(self, weather_data):
        """
        天気と季節に基づいて設定を推奨する

        引数:
            weather_data: 天気予報データ

        戻り値:
            推奨設定情報 (season, setting_type, settings_values)
        """
        detailed_season = get_detailed_season()
        today_weather = weather_data['today']['weather']
        tomorrow_weather = weather_data['tomorrow']['weather']
        rainy_days = 0
        if '雨' in today_weather or '雪' in today_weather:
            rainy_days += 1
        if '雨' in tomorrow_weather or '雪' in tomorrow_weather:
            rainy_days += 1
        setting_type = 'typeA' if rainy_days > 0 else 'typeB'
        settings_values = self.settings_manager.get_season_settings(detailed_season, setting_type)
        if 'warnings' in weather_data and weather_data['warnings']:
            setting_type = 'typeA'
            settings_values = self.settings_manager.get_season_settings(detailed_season, setting_type)
        return (detailed_season, setting_type, settings_values)