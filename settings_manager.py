import logging
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys


class SettingsManager:
    """設定を一元管理するクラス"""

    _instance = None
    _settings = None

    def __new__(cls):
        """シングルトンパターンの実装"""
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            cls._instance._load_settings()
        return cls._instance

    def _load_settings(self):
        """設定ファイルを読み込む"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            settings_path = os.path.join(base_dir, 'settings.json')

            with open(settings_path, 'r', encoding='utf-8') as f:
                self._settings = json.load(f)

            print("設定ファイルを読み込みました")
        except Exception as e:
            print(f"設定ファイルの読み込みエラー: {str(e)}")
            sys.exit(1)

    def save_settings(self):
        """設定をファイルに保存する"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            settings_path = os.path.join(base_dir, 'settings.json')

            # バックアップを作成
            backup_path = f"{settings_path}.bak"
            try:
                with open(settings_path, 'r', encoding='utf-8') as src:
                    with open(backup_path, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
                print(f"設定ファイルのバックアップを作成: {backup_path}")
            except Exception as e:
                print(f"バックアップ作成エラー: {str(e)}")

            # 設定を保存
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, ensure_ascii=False, indent=2)

            print("設定ファイルを保存しました")
            return True
        except Exception as e:
            print(f"設定ファイルの保存エラー: {str(e)}")
            return False

    def get_inverter_parameters(self):
        """インバーターのパラメータIDを取得"""
        return self._settings.get("inverter_parameters", {})

    def get_season_settings(self, season, setting_type):
        """季節と設定タイプに基づいた設定値を取得"""
        # 詳細な季節設定から基本季節へのマッピングを取得
        detailed_map = self._settings.get("detailed_seasonal_settings", {})
        basic_season = detailed_map.get(season, {}).get("reference", season)

        # 基本季節の設定を取得
        seasonal_settings = self._settings.get("seasonal_settings", {})
        season_data = seasonal_settings.get(basic_season, {})

        # 設定タイプの値を取得
        return season_data.get(setting_type, {})

    def get_weather_icon(self, weather):
        """天気に対応するアイコンを取得"""
        weather_icons = self._settings.get("weather_icons", {})
        for key, icon in weather_icons.items():
            if key in weather:
                return icon
        return "🌐"

    def get_season_icon(self, season):
        """季節に対応するアイコンを取得"""
        return self._settings.get("season_icons", {}).get(season, "🌐")

    def get_email_template(self):
        """メールテンプレートを取得"""
        return self._settings.get("notification", {}).get("email", {}).get("template", {})

    def get_line_template(self):
        """LINEテンプレートを取得"""
        return self._settings.get("notification", {}).get("line", {}).get("template", {})

    def is_email_enabled(self):
        """メール通知が有効かどうか"""
        return self._settings.get("notification", {}).get("email", {}).get("enabled", False)

    def is_line_enabled(self):
        """LINE通知が有効かどうか"""
        return self._settings.get("notification", {}).get("line", {}).get("enabled", False)

    def update_season_settings(self, season, setting_type, new_values):
        """季節と設定タイプに基づいた設定値を更新"""
        # 詳細な季節設定から基本季節へのマッピングを取得
        detailed_map = self._settings.get("detailed_seasonal_settings", {})
        basic_season = detailed_map.get(season, {}).get("reference", season)

        if basic_season in self._settings.get("seasonal_settings", {}):
            if setting_type in self._settings["seasonal_settings"][basic_season]:
                self._settings["seasonal_settings"][basic_season][setting_type].update(
                    new_values)
                return True
        return False

    def get_weather_connectors(self):
        """天気の接続詞パターンを取得"""
        return self._settings.get("weather_connectors", [
            "　後　", "　のち　", "　時々　", "　一時　",
            "　夜　", "　夜遅く　", "　所により　",
            "　で　", "　から　", "　または　"
        ])

    def get(self, key, default=None):
        """設定値を取得するためのメソッド"""
        return self._settings.get(key, default)

    @property  
    def settings(self):
        """下位互換性のための settings プロパティ"""
        return self._settings
