import logging
from requests import post
from datetime import datetime

from src import _config


class DiscordHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()

    def emit(self, record: logging.LogRecord) -> None:
        data = { "embeds": [{
                    "title": "Новая информация",
                    "description": f"!{record.levelname}\n\n{self.format(record)}",
                    "thumbnail": { "url": record.__dict__.get("user_avatar", None) },
                    "footer": { "text": datetime.now().strftime("%d %B %Y — %H:%M") }
            }] }
        post(_config.LOG_WEBHOOK, json=data)


# _formatter = logging.Formatter(u'[%(asctime)s] %(levelname)s — %(message)s')


def get_logger() -> logging.Logger:
    return logging.getLogger(_config.APP_NAME)


def _create_logger() -> None:
    level = logging.DEBUG if _config.DEBUG else logging.INFO

    logger = logging.getLogger(_config.APP_NAME)
    logger.setLevel(level=level)
    
    discord_handler = DiscordHandler()
    discord_handler.setLevel(logging.INFO)
    logger.addHandler(discord_handler)


def setup_logger() -> None:
    _create_logger()