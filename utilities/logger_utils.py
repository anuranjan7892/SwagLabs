import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name="test_logger"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "report")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "logfile.log")

        file_handler = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s.%(funcName)s() - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Optional: also add console handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger