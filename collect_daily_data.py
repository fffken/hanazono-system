import os
import sys
import json
import datetime
import logging
from solarman_api_client import SolarmanAPIClient
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('collect_data.log'), logging.StreamHandler()])
logger = logging.getLogger('collector')

def collect_yesterday_data():
    """前日のデータ収集"""
    yesterday = datetime.datetime.now().date() - datetime.timedelta(days=1)
    date_str = yesterday.strftime('%Y-%m-%d')
    logger.info(f'{date_str}のデータ収集を開始します')
    client = SolarmanAPIClient()
    if not client.login():
        logger.error('ログインに失敗しました')
        return False
    success = True
    station_id = client.config.get('station_id')
    station_stats_url = f'{client.base_url}/user-s/app/pss/ps/{station_id}/real-data'
    try:
        response = client.session.get(station_stats_url)
        if response.status_code == 200:
            stats_data = response.json()
            client.save_data(stats_data, f'station_stats_{date_str}.json')
            logger.info('発電所の統計情報を取得しました')
        else:
            logger.error(f'発電所の統計情報取得失敗: {response.status_code}')
            success = False
    except Exception as e:
        logger.error(f'発電所の統計情報取得エラー: {str(e)}')
        success = False
    daily_data = client.get_daily_data(yesterday)
    if daily_data:
        client.save_data(daily_data, f'daily_data_{date_str}.json')
    else:
        logger.error('日次データの取得に失敗しました')
        success = False
    battery_soc = client.get_param_history('B_left_cap1', yesterday)
    if battery_soc:
        client.save_data(battery_soc, f'battery_soc_{date_str}.json')
    else:
        logger.error('バッテリーSOC履歴の取得に失敗しました')
        success = False
    generation = client.get_param_history('PVDE', yesterday)
    if generation:
        client.save_data(generation, f'generation_{date_str}.json')
    else:
        logger.error('発電量履歴の取得に失敗しました')
        success = False
    consumption = client.get_param_history('Etdy_use1', yesterday)
    if consumption:
        client.save_data(consumption, f'consumption_{date_str}.json')
    else:
        logger.error('消費電力履歴の取得に失敗しました')
        success = False
    charging = client.get_param_history('Etdy_cg1', yesterday)
    if charging:
        client.save_data(charging, f'charging_{date_str}.json')
    else:
        logger.error('充電履歴の取得に失敗しました')
        success = False
    discharging = client.get_param_history('Etdy_dcg1', yesterday)
    if discharging:
        client.save_data(discharging, f'discharging_{date_str}.json')
    else:
        logger.error('放電履歴の取得に失敗しました')
        success = False
    if success:
        logger.info(f'{date_str}のデータ収集が完了しました')
    else:
        logger.warning(f'{date_str}のデータ収集は一部失敗しました')
    return success
if __name__ == '__main__':
    collect_yesterday_data()