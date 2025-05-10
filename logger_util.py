import logging
import logging.handlers
import os

# Define log directory relative to the script's location
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
MAIN_LOG_FILE = os.path.join(LOG_DIR, 'hanazono.log')
ERROR_LOG_FILE = os.path.join(LOG_DIR, 'hanazono_error.log')

# Ensure log directory exists - create if it doesn't
# Using exist_ok=True prevents errors if directory already exists
os.makedirs(LOG_DIR, exist_ok=True)

# ロガーインスタンスをファイルスコープで保持（シングルトンのように振る舞う）
_hanazono_logger_instance = None

def setup_logger(log_level=logging.INFO):
  """
  Sets up and returns the Hanazono project logger instance.
  Configures handlers for general info logs (rotating) and error logs (separate file).
  Ensures handlers are added only once.

  Args:
    log_level: 設定するログレベル (例: logging.INFO, logging.DEBUG)
  """
  global _hanazono_logger_instance

  # ロガーが既に設定されている場合は、レベルだけ更新して返す
  if _hanazono_logger_instance is not None:
    _hanazono_logger_instance.setLevel(log_level)
    return _hanazono_logger_instance

  # ロガーインスタンスを取得 (名前付きロガー)
  logger = logging.getLogger('hanazono_logger')

  # ハンドラがまだ設定されていない場合のみ、ハンドラとフォーマッターを設定
  if not logger.hasHandlers():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # --- Main Log File Handler (Rotating) ---
    main_file_handler = logging.handlers.RotatingFileHandler(
      MAIN_LOG_FILE,
      maxBytes=1024 * 1024, # 1MB per file
      backupCount=5   # Keep 5 backup files
    )
    main_file_handler.setLevel(logging.INFO) # このハンドラはINFOレベル以上のメッセージを処理
    main_file_handler.setFormatter(formatter)
    logger.addHandler(main_file_handler)

    # --- Error Log File Handler ---
    error_file_handler = logging.FileHandler(ERROR_LOG_FILE)
    error_file_handler.setLevel(logging.ERROR) # このハンドラはERRORレベル以上のメッセージを処理
    error_file_handler.setFormatter(formatter)
    logger.addHandler(error_file_handler)

  # ロガーの全体レベルを設定
  logger.setLevel(log_level)

  # ロガーインスタンスをファイルスコープ変数に保持
  _hanazono_logger_instance = logger

  return logger

# Example of how to use the logger elsewhere:
# from logger_util import setup_logger
# hanazono_log = setup_logger() # デフォルトはINFOレベル
# hanazono_log_debug = setup_logger(logging.DEBUG) # DEBUGレベルで取得（既存のハンドラは再利用される）
# hanazono_log.info("System started.")
# try:
#  # Some operation that might fail
#  pass
# except Exception as e:
#  hanazono_log.error(f"An error occurred: {e}", exc_info=True) # exc_info adds traceback for errors
