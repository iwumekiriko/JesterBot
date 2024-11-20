import logging
from requests import post

from src import _config


class DiscordHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()

    def emit(self, record) -> None:
        data = { "embeds": [{
                    "title": "log",
                    "description": _formatter.format(record)
            }] }
        post(_config.LOG_WEBHOOK, json=data)


_formatter = logging.Formatter(u'[%(asctime)s] %(levelname)s — %(message)s')


def get_logger() -> logging.Logger:
    return logging.getLogger(_config.APP_NAME)


def _create_logger() -> None:
    level = logging.DEBUG if _config.DEBUG else logging.INFO

    logger = logging.getLogger(_config.APP_NAME)
    logger.setLevel(level=level)
    
    handler = DiscordHandler()
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    handler.setFormatter(_formatter)


def setup_logger() -> None:
    _create_logger()