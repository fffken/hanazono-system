#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

def get_current_season():
    """
    現在の月から季節を判定する
    戻り値: 'winter', 'spring_fall', 'summer'のいずれか
    """
    current_month = datetime.datetime.now().month
    
    if current_month in [12, 1, 2, 3]:
        return "winter"
    elif current_month in [4, 5, 6, 10, 11]:
        return "spring_fall"
    else:  # 7, 8, 9月
        return "summer"

def get_detailed_season():
    """
    現在の日付から詳細な季節を判定する
    戻り値: 詳細な季節コード（'winter_early', 'spring_mid'など）
    """
    now = datetime.datetime.now()
    month = now.month
    day = now.day
    
    # 月ごとに季節を詳細に判定
    if month == 1:  # 1月
        return "winter_mid"
    elif month == 2:  # 2月
        return "winter_late"
    elif month == 3:  # 3月
        if day < 21:  # 春分の日（約3月21日）前
            return "winter_late"
        else:
            return "spring_early"
    elif month == 4:  # 4月
        return "spring_early"
    elif month == 5:  # 5月
        return "spring_mid"
    elif month == 6:  # 6月
        if day < 15:  # 梅雨入り目安
            return "spring_late"
        else:
            return "rainy"
    elif month == 7:  # 7月
        if day < 15:  # 梅雨明け目安
            return "rainy"
        else:
            return "summer_early"
    elif month == 8:  # 8月
        return "summer_mid"
    elif month == 9:  # 9月
        if day < 23:  # 秋分の日（約9月23日）前
            return "summer_late"
        else:
            return "autumn_early"
    elif month == 10:  # 10月
        return "autumn_early"
    elif month == 11:  # 11月
        return "autumn_mid"
    else:  # 12月
        return "winter_early"

def get_season_name(season_code):
    """
    季節コードから日本語の季節名を取得
    
    引数:
        season_code: 季節コード
    戻り値:
        日本語の季節名
    """
    season_names = {
        "winter_early": "初冬",
        "winter_mid": "真冬",
        "winter_late": "晩冬",
        "spring_early": "早春",
        "spring_mid": "春",
        "spring_late": "晩春",
        "rainy": "梅雨",
        "summer_early": "初夏",
        "summer_mid": "真夏",
        "summer_late": "晩夏",
        "autumn_early": "初秋",
        "autumn_mid": "秋",
        "autumn_late": "晩秋",
        
        # 後方互換性のための名称
        "winter": "冬季",
        "spring_fall": "春秋季",
        "summer": "夏季"
    }
    
    return season_names.get(season_code, "不明")
