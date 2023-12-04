import logging
from typing import Any


def setup_logging() -> Any:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('data_file.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    file_formatter = logging.Formatter('%(asctime)s %(name)s %(funcName)s %(levelname)s: %(message)s')
    file_handler.setFormatter(file_formatter)

    logger.addHandler(file_handler)
    return logger
