# coding=utf-8
import logging
import os
import sys

from utils.functions import str2bool

ERROR_404_HELP = False

SECRET_KEY = os.getenv('SECRET_KEY') or 'dce_autoscale_plugin'

SOURCE_ROOT = os.path.abspath(os.path.dirname(__file__))

API_VERSION = '0.1'
ENABLE_CORS = True
PROD = str2bool(os.getenv('PROD'), False)
GUNICORN_WORKERS = os.getenv('GUNICORN_WORKERS')

LOG_LEVEL = logging.INFO if PROD else logging.DEBUG
LOG_FORMAT = '%(asctime)s (%(process)d/%(threadName)s) %(name)s %(levelname)s - %(message)s'


def setup_logging(level=None):
    level = level or LOG_LEVEL
    console_handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(level)
    # Disable requests logging
    logging.getLogger("requests").propagate = False
    logging.getLogger("docker.auth").setLevel(logging.INFO)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)


THREAD_POOL_SIZE = int(os.getenv('THREAD_POOL_SIZE', 20))
THREAD_POOL_TIMEOUT = int(os.getenv('THREAD_POOL_TIMEOUT', 120))

REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))

DEFAULT_POLL_INTERVAL = 30
MONITOR_LIFE_TIME = 30 * 60  # 半小时，监控进程的存活时间，定期重启监控进程

DEFAULT_MIN_REPLICAS = 1

