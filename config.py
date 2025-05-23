#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 気象情報の取得設定
WEATHER_URL = "https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=370000"
WEATHER_API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/370000.json"

# メール通知設定
EMAIL_ENABLED = True
EMAIL_SENDER = "fffken@gmail.com"  # 送信元メールアドレス
EMAIL_PASSWORD = "bbzpgdsvqlcemyxi"  # Gmailのアプリパスワード
EMAIL_RECEIVERS = ["fffken@gmail.com"]  # 通知先メールアドレス
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587

# インバーター設定パラメータID
CHARGE_CURRENT_ID = "07"
CHARGE_TIME_ID = "10"
SOC_SETTING_ID = "62"

# タイプA/B設定（季節ごと）
SETTINGS = {
    "winter": {  # 12-3月
        "typeA": {"charge_current": 50, "charge_time": 45, "soc": 50},
        "typeB": {"charge_current": 60, "charge_time": 60, "soc": 60}
    },
    "spring_fall": {  # 4-6月、10-11月
        "typeA": {"charge_current": 40, "charge_time": 30, "soc": 35},
        "typeB": {"charge_current": 50, "charge_time": 45, "soc": 45}
    },
    "summer": {  # 7-9月
        "typeA": {"charge_current": 25, "charge_time": 15, "soc": 25},
        "typeB": {"charge_current": 35, "charge_time": 30, "soc": 35}
    }
}

# 天気条件によるタイプ選択ルール
WEATHER_TYPE_MAPPING = {
    "晴": "typeB",       # 晴れの場合はタイプB（充電を強化）
    "晴時々曇": "typeB",
    "晴一時曇": "typeB",
    "晴のち曇": "typeB",
    "曇時々晴": "typeB",
    "曇一時晴": "typeB",
    "曇のち晴": "typeB",
    "曇": "typeA",       # 曇りの場合はタイプA（控えめに充電）
    "曇時々雨": "typeA",
    "曇一時雨": "typeA",
    "曇のち雨": "typeA",
    "雨": "typeA",       # 雨の場合はタイプA
    "雨時々曇": "typeA",
    "雨一時曇": "typeA",
    "雨のち曇": "typeA",
    "雨時々晴": "typeA",
    "雨一時晴": "typeA",
    "雨のち晴": "typeA"
}

# ログファイルパス
LOG_FILE = "solar_control.log"

# デフォルト設定（エラー発生時など）
DEFAULT_TYPE = "typeA"
# 警報・注意報のAPI URL (香川県)
WARNING_API_URL = "https://www.jma.go.jp/bosai/warning/data/warning/370000.json"

# 台風情報のAPI URL
TYPHOON_API_URL = "https://www.jma.go.jp/bosai/typhoon/data/latest.json"

# 警報・注意報と絵文字のマッピング
WARNING_EMOJI = {
    # 警報
    "警報": "⚠️",
    "大雨警報": "⛈️",
    "洪水警報": "🌊",
    "暴風警報": "🌪️",
    "暴風雪警報": "❄️🌪️",
    "大雪警報": "❄️",
    "波浪警報": "🌊",
    "高潮警報": "🌊",

    # 注意報
    "注意報": "⚠️",
    "大雨注意報": "☔",
    "洪水注意報": "💧",
    "強風注意報": "💨",
    "風雪注意報": "❄️💨",
    "大雪注意報": "❄️",
    "波浪注意報": "🌊",
    "高潮注意報": "🌊",
    "雷注意報": "⚡",
    "融雪注意報": "💧",
    "濃霧注意報": "🌫️",
    "乾燥注意報": "🔥",
    "なだれ注意報": "⛄",
    "低温注意報": "❄️",
    "霜注意報": "❄️",
    "着氷注意報": "❄️",
    "着雪注意報": "❄️",

    # 特別警報
    "特別警報": "🚨",
    "大雨特別警報": "🚨⛈️",
    "暴風特別警報": "🚨🌪️",
    "高潮特別警報": "🚨🌊",
    "波浪特別警報": "🚨🌊",
    "暴風雪特別警報": "🚨❄️🌪️",
    "大雪特別警報": "🚨❄️",

    # その他
    "解除": "✅"
}

# 台風関連の絵文字
TYPHOON_EMOJI = "🌀"
# 詳細な季節と絵文字のマッピング
DETAILED_SEASON_EMOJI = {
    "winter_early": "🍂❄️",  # 初冬 (12月)
    "winter_mid": "❄️☃️",  # 真冬 (1月)
    "winter_late": "❄️🌱",  # 晩冬 (2-3月)
    "spring_early": "🌸🌱",  # 早春 (3-4月)
    "spring_mid": "🌸🌷",  # 春 (4-5月)
    "spring_late": "🌿🌦️",  # 晩春 (5-6月)
    "rainy": "☔🌿",  # 梅雨 (6月中旬-7月中旬)
    "summer_early": "☀️🌿",  # 初夏 (7月)
    "summer_mid": "☀️🏖️",  # 真夏 (8月)
    "summer_late": "☀️🍃",  # 晩夏 (9月)
    "autumn_early": "🍁🍃",  # 初秋 (9-10月)
    "autumn_mid": "🍂🍁",  # 秋 (10-11月)
    "autumn_late": "🍂❄️"  # 晩秋 (11-12月)
}
