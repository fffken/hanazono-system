import logging
import logging.handlers
import os
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
MAIN_LOG_FILE = os.path.join(LOG_DIR, 'hanazono.log')
ERROR_LOG_FILE = os.path.join(LOG_DIR, 'hanazono_error.log')
os.makedirs(LOG_DIR, exist_ok=True)
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
    if _hanazono_logger_instance is not None:
        _hanazono_logger_instance.setLevel(log_level)
        return _hanazono_logger_instance
    logger = logging.getLogger('hanazono_logger')
    if not logger.hasHandlers():
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        main_file_handler = logging.handlers.RotatingFileHandler(MAIN_LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
        main_file_handler.setLevel(logging.INFO)
        main_file_handler.setFormatter(formatter)
        logger.addHandler(main_file_handler)
        error_file_handler = logging.FileHandler(ERROR_LOG_FILE)
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(formatter)
        logger.addHandler(error_file_handler)
    logger.setLevel(log_level)
    _hanazono_logger_instance = logger
    return logger