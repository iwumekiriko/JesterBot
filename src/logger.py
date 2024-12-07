import logging
from requests import post

from src import settings
from src.utils._time import current_time
from src.utils._exceptions import LogWebhooksNotSetException


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
    "message": "messages_webhook_url",
    "command_interaction": "command_interactions_webhook_url",
    "ticket": "tickets_webhook_url",
    "members": "members_webhook_url",
    "guild": "guild_webhook_url",
    "else": "else_webhook_url",
}


class DiscordHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()

    def emit(self, record: logging.LogRecord) -> None:
        from src.config import cfg
        params = record.__dict__

        data = { "embeds": [{
                    "description": f"# {embed_titles[record.levelname]}\n\n{self.format(record)}",
                    "thumbnail": { "url": params.get("user_avatar", None) },
                    "footer": { "text": current_time().strftime("%d %B %Y — %H:%M") },
                    "color": embed_colors[record.levelname],
            }] }
        
        try:
            webhook_url = getattr(cfg.webhooks_cfg(
                params.get("guild_id", cfg.base_guild_id)),
                log_webhooks[params.get("type", "else")])
            post(webhook_url, json=data)
        except:
            print("Не настроен вебхук для логов! [/config]")


def get_logger() -> logging.Logger:
    return logging.getLogger(settings.APP_NAME)


def _create_logger() -> None:
    level = logging.DEBUG if settings.DEBUG else logging.INFO

    logger = logging.getLogger(settings.APP_NAME)
    logger.setLevel(level=level)
    
    discord_handler = DiscordHandler()
    discord_handler.setLevel(level)
    logger.addHandler(discord_handler)


def setup_logger() -> None:
    _create_logger()