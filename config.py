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
