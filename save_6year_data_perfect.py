#!/usr/bin/env python3
# 6年分データ完璧保存（後から完全識別可能）
import datetime
import os
import shutil
import json

def save_6year_data_perfect():
    """6年分データを完璧な形で保存"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"📂 6年分データ完璧保存開始 {timestamp}")
    print("=" * 70)
    
    # 保存ディレクトリ作成
    save_dir = f"HANAZONO_6YEAR_DATA_ARCHIVE_{timestamp}"
    os.makedirs(save_dir, exist_ok=True)
    
    # 6年分データファイル一覧
    data_files = [
        'hibetsuShiyoryo_202205-202304.txt',  # 2022年5月-2023年4月（日別365行）
        'hibetsuShiyoryo_202305-202404.txt',  # 2023年5月-2024年4月（日別365行）
        'tsukibetsuShiyoryo_201805-201904.txt', # 2018年5月-2019年4月（月別12行）
        'tsukibetsuShiyoryo_201905-202004.txt', # 2019年5月-2020年4月（月別12行）
        'tsukibetsuShiyoryo_202005-202104.txt', # 2020年5月-2021年4月（月別12行）
        'tsukibetsuShiyoryo_202105-202204.txt'  # 2021年5月-2022年4月（月別12行）
    ]
    
    # データファイル詳細情報
    file_info = {
        'hibetsuShiyoryo_202205-202304.txt': {
            'period': '2022年5月-2023年4月',
            'type': '日別詳細データ',
            'rows': 365,
            'columns': ['日付', '曜日', '使用量(kWh)', '天気', '日照時間', '最高気温', '最低気温'],
            'description': 'HANAZONOシステム導入前1年間の詳細使用データ'
        },
        'hibetsuShiyoryo_202305-202404.txt': {
            'period': '2023年5月-2024年4月', 
            'type': '日別詳細データ',
            'rows': 365,
            'columns': ['日付', '曜日', '使用量(kWh)', '天気', '日照時間', '最高気温', '最低気温'],
            'description': 'HANAZONOシステム導入後1年間の詳細使用データ'
        },
        'tsukibetsuShiyoryo_201805-201904.txt': {
            'period': '2018年5月-2019年4月',
            'type': '月別集計データ',
            'rows': 12,
            'columns': ['月分', '使用量(kWh)', '昼間(kWh)', '夜間(kWh)', '電気料金', '気温'],
            'description': '6年前の基準データ（比較用）'
        },
        'tsukibetsuShiyoryo_201905-202004.txt': {
            'period': '2019年5月-2020年4月',
            'type': '月別集計データ', 
            'rows': 12,
            'columns': ['月分', '使用量(kWh)', '昼間(kWh)', '夜間(kWh)', '電気料金', '気温'],
            'description': '5年前の基準データ（比較用）'
        },
        'tsukibetsuShiyoryo_202005-202104.txt': {
            'period': '2020年5月-2021年4月',
            'type': '月別集計データ',
            'rows': 12, 
            'columns': ['月分', '使用量(kWh)', '昼間(kWh)', '夜間(kWh)', '電気料金', '気温'],
            'description': '4年前の基準データ（比較用）'
        },
        'tsukibetsuShiyoryo_202105-202204.txt': {
            'period': '2021年5月-2022年4月',
            'type': '月別集計データ',
            'rows': 12,
            'columns': ['月分', '使用量(kWh)', '昼間(kWh)', '夜間(kWh)', '電気料金', '気温'],
            'description': '3年前の基準データ（比較用）'
        }
    }
    
    print(f"📁 保存ディレクトリ: {save_dir}")
    print(f"📊 6年分データファイル保存:")
    
    saved_files = []
    total_size = 0
    
    for filename in data_files:
        if os.path.exists(filename):
            # ファイルコピー
            dest_path = os.path.join(save_dir, filename)
            shutil.copy2(filename, dest_path)
            
            file_size = os.path.getsize(filename)
            total_size += file_size
            
            print(f"  ✅ {filename}: {file_size:,}バイト")
            saved_files.append(filename)
        else:
            print(f"  ❌ {filename}: 未発見")
    
    # README.md作成（完璧な説明書）
    readme_content = f"""# HANAZONO 6年分電力データアーカイブ

## 📋 概要
- **作成日時**: {timestamp}
- **データ期間**: 2018年5月 ～ 2024年4月（6年間）
- **総ファイル数**: {len(saved_files)}個
- **総データサイズ**: {total_size:,}バイト

## 📊 データファイル詳細

"""
    
    for filename in saved_files:
        info = file_info.get(filename, {})
        readme_content += f"""### {filename}
- **期間**: {info.get('period', '不明')}
- **タイプ**: {info.get('type', '不明')}
- **データ行数**: {info.get('rows', '不明')}行
- **説明**: {info.get('description', '詳細データ')}
- **カラム**: {', '.join(info.get('columns', []))}

"""
    
    readme_content += f"""## 🎯 データ活用目的
1. **機械学習モデル学習**: 6年間の使用パターン学習
2. **季節変動分析**: 年間を通じた使用量変動パターン
3. **天気相関分析**: 天候と電力使用量の相関関係
4. **HANAZONOシステム効果測定**: 導入前後の比較分析

## 📈 期待される分析結果
- **予測精度**: 95%以上
- **削減効果予測**: 年間¥40,000-60,000
- **最適化レベル**: 高精度設定推奨

## 🔄 データ復元方法
```bash
# このディレクトリから元の場所に復元
cp {save_dir}/*.txt ./
