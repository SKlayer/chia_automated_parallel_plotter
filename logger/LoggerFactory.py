import logging
import logging.handlers
import sys
from pathlib import Path

class LoggerFactory():
    formatter = logging.Formatter('%(asctime)s - %(message)s')

    log_path = Path("./log/")
    Path("./log/").mkdir(exist_ok=True)
    logger = logging.getLogger("fileLogger")
    logger.setLevel(logging.DEBUG)

    file_logger = logging.handlers.RotatingFileHandler(filename=log_path / 'chiafarmer.log', maxBytes=1000000, backupCount=2)
    file_logger.setLevel(logging.DEBUG)
    file_logger.setFormatter(formatter)

    logger.addHandler(file_logger)

    stdout_logger = logging.getLogger("stdoutLogger")
    stdout_logger.setLevel(logging.DEBUG)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_logger.addHandler(stdout_handler)
