import os
import logging
from logging.handlers import RotatingFileHandler
from django.conf import settings

def get_logger(file_path='djangosh/logs/system-log.log', log_level=logging.INFO):
  log_file = (settings.BASE_DIR/file_path)
  os.makedirs(log_file.parent, exist_ok=True)
  handler = RotatingFileHandler(log_file.as_posix(), mode='a+', maxBytes=1024*1024, backupCount=10)
  handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
  logger = logging.getLogger(__name__)
  logger.setLevel(log_level)
  logger.addHandler(handler)
  print(f"!> logger: {logger}")
  return logger

logger = get_logger(log_level=logging.INFO)
