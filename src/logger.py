import logging
from requests import post
from datetime import datetime

from src import _config


embed_colors = {
    "ERROR": 0x8b0000,
    "INFO": 0x90ee90,
    "WARNING": 0xffd700,
    "CRITICAL": 0xff0000,
    "DEBUG": 0x00bffff
}

embed_titles = {
    "ERROR": "ОШИБКА",
    "INFO": "ИНФОРМАЦИЯ",
    "WARNING": "ПРЕДУПРЕЖДЕНИЕ",
    "CRITICAL": "КРИТИЧЕСКАЯ ОШИБКА",
    "DEBUG": "ДЕБАГ"
}

log_webhooks = {
    "message": _config.MESSAGE_WEBHOOK,
    "command_interaction": _config.COMMAND_INTERACTIONS_WEBHOOK,
    "ticket": _config.TICKET_WEBHOOK,
    "members": _config.MEMBER_WEBHOOK,
    "guild": _config.GUILD_WEBHOOK,
    "else": _config.ELSE_WEBHOOK,
}


class DiscordHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()

    def emit(self, record: logging.LogRecord) -> None:
        data = { "embeds": [{
                    "description": f"# {embed_titles[record.levelname]}\n\n{self.format(record)}",
                    "thumbnail": { "url": record.__dict__.get("user_avatar", None) },
                    "footer": { "text": datetime.now().strftime("%d %B %Y — %H:%M") },
                    "color": embed_colors[record.levelname]
            }] }
        post(log_webhooks[record.__dict__.get("type", "else")], json=data)


def get_logger() -> logging.Logger:
    return logging.getLogger(_config.APP_NAME)


def _create_logger() -> None:
    level = logging.DEBUG if _config.DEBUG else logging.INFO

    logger = logging.getLogger(_config.APP_NAME)
    logger.setLevel(level=level)
    
    discord_handler = DiscordHandler()
    discord_handler.setLevel(level)
    logger.addHandler(discord_handler)


def setup_logger() -> None:
    _create_logger()