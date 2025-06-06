"""データファイル操作ユーティリティ"""
import os
import logging
from datetime import datetime, timedelta
logger = logging.getLogger('data_util')

def find_latest_data_file(target_date_str=None, data_dir='data', prefix='lvyuan_data_', ext='.csv'):
    """
    指定した日付のデータファイルを検索し、見つからない場合は
    利用可能な最新のデータファイルを返す

    Args:
        target_date_str: 検索する日付（YYYYMMDD形式、Noneなら前日）
        data_dir: データファイルの保存ディレクトリ
        prefix: データファイル名のプレフィックス
        ext: データファイルの拡張子

    Returns:
        最新のデータファイルパスとその日付、またはNoneとNone
    """
    if target_date_str is None:
        yesterday = datetime.now() - timedelta(days=1)
        target_date_str = yesterday.strftime('%Y%m%d')
    target_file = os.path.join(data_dir, f'{prefix}{target_date_str}{ext}')
    if os.path.exists(target_file):
        logger.info(f'指定日付 {target_date_str} のデータファイルを使用します: {target_file}')
        return (target_file, target_date_str)
    logger.warning(f'指定日付 {target_date_str} のデータファイルが見つかりません。他の日付を検索します。')
    data_files = []
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.startswith(prefix) and file.endswith(ext):
                try:
                    date_str = file[len(prefix):].split('.')[0]
                    if len(date_str) == 8 and date_str.isdigit():
                        data_files.append((file, date_str))
                except (IndexError, ValueError):
                    continue
    if data_files:
        data_files.sort(key=lambda x: x[1], reverse=True)
        latest_file = os.path.join(data_dir, data_files[0][0])
        latest_date = data_files[0][1]
        logger.warning(f'最新のデータファイルを発見: {latest_file} (日付: {latest_date})')
        return (latest_file, latest_date)
    logger.error(f'利用可能なデータファイルが見つかりませんでした。ディレクトリ: {data_dir}')
    return (None, None)

def format_date_jp(date_str):
    """日付を日本語形式にフォーマットする（YYYYMMDD → YYYY年MM月DD日）"""
    try:
        year = date_str[:4]
        month = date_str[4:6].lstrip('0')
        day = date_str[6:8].lstrip('0')
        return f'{year}年{month}月{day}日'
    except (IndexError, TypeError):
        return '不明'