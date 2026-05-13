import json
import logging
import sys
from requests import post, exceptions
from logging import Formatter, StreamHandler
from asyncio import Queue

from src import settings
from src.utils._time import current_time
from src.utils._exceptions import LoggerException
from src.models.logs import Log, LogLevel


CONSOLE_COLORS = {
    'DEBUG': '\033[96m',
    'INFO': '\033[92m',
    'WARNING': '\033[93m',
    'ERROR': '\033[91m',
    'CRITICAL': '\033[41m'
}

RESET = '\033[0m'

_queue = Queue()


class DiscordFilter(logging.Filter):
    def filter(self, record):
        return hasattr(record, 'type')


class ConsoleFilter(logging.Filter):
    def filter(self, record):
        return not hasattr(record, 'type')


class ColoredFormatter(Formatter):
    def format(self, record):
        levelname = record.levelname
        color = CONSOLE_COLORS.get(levelname, '')
        
        time_str = current_time().strftime("[%a %b %d %H:%M:%S %Y]")
        level_str = f"{color}{levelname}{RESET}"
        message = super().format(record)
        return f"{time_str}: {level_str} - {message}"


class DiscordHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.addFilter(DiscordFilter())

    def emit(self, record: logging.LogRecord) -> None:
        params = record.__dict__
        log = Log(
            guild_id = params.get("guild_id", 0),
            level = LogLevel[record.levelname],
            message = self.format(record),
            category = params.get("type", "else"),
            avatar_url = params.get("user_avatar", None),
            images_urls = params.get("images_urls", []),
            files_urls = params.get("files_urls", [])
        )

        _queue.put_nowait(log)


def get_logger() -> logging.Logger:
    return logging.getLogger(settings.APP_NAME)


async def start_log_worker():
    from ._api_interaction import send_log_to_api
    while True:
        log = await _queue.get()
        try:
            await send_log_to_api(log)
        except Exception as e:
            print(f"!!! Failed to send log: {e}")


def _create_logger() -> None:
    level = logging.DEBUG if settings.DEBUG else logging.INFO

    logger = logging.getLogger(settings.APP_NAME)
    logger.setLevel(level=level)
    
    discord_handler = DiscordHandler()
    discord_handler.setLevel(level)

    console_handler = StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.addFilter(ConsoleFilter())
    console_handler.setFormatter(ColoredFormatter('%(message)s'))

    logger.addHandler(console_handler)
    logger.addHandler(discord_handler)


def setup_logger() -> None:
    _create_logger()