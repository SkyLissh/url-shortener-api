import logging
import multiprocessing
import os

from tabulate import tabulate

log = logging.getLogger(__name__)

host = os.getenv("API_HOST", "0.0.0.0")
port = os.getenv("API_PORT", "8000")
bind = os.getenv("API_BIND", f"{host}:{port}")

workers = os.getenv("API_WORKERS", 6)
worker_tmp_dir = "/dev/shm"

loglevel = os.getenv("API_LOG_LEVEL", "info")
accesslog_var = os.getenv("ACCESS_LOG", "-")
accesslog = accesslog_var or None
errorlog_var = os.getenv("ERROR_LOG", "-")
errorlog = errorlog_var or None

graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "120")
timeout_str = os.getenv("TIMEOUT", "120")
keepalive_str = os.getenv("KEEP_ALIVE", "5")

print(f"Cores: {multiprocessing.cpu_count()}")

log.info(
    """
    ░██████╗░██╗░░░██╗███╗░░██╗██╗░█████╗░░█████╗░██████╗░███╗░░██╗
    ██╔════╝░██║░░░██║████╗░██║██║██╔══██╗██╔══██╗██╔══██╗████╗░██║
    ██║░░██╗░██║░░░██║██╔██╗██║██║██║░░╚═╝██║░░██║██████╔╝██╔██╗██║
    ██║░░╚██╗██║░░░██║██║╚████║██║██║░░██╗██║░░██║██╔══██╗██║╚████║
    ╚██████╔╝╚██████╔╝██║░╚███║██║╚█████╔╝╚█████╔╝██║░░██║██║░╚███║
    ░╚═════╝░░╚═════╝░╚═╝░░╚══╝╚═╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚══╝
    """
)

table_rows = [
    ("Host", host),
    ("Port", port),
    ("Workers", workers),
    ("Log Level", loglevel),
    ("Access Log", accesslog),
    ("Error Log", errorlog),
    ("Graceful Timeout", graceful_timeout_str),
    ("Timeout", timeout_str),
    ("Keep Alive", keepalive_str),
]

log.info(tabulate(table_rows, headers=["Name", "Value"]))
