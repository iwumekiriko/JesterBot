import json
import logging
from requests import post, exceptions

from src import settings
from src.utils._time import current_time
from src.utils._exceptions import LoggerException


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
    "voice": "voice_webhook_url",
    "else": "else_webhook_url",
}


class DiscordHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()

    def emit(self, record: logging.LogRecord) -> None:
        from src.config import cfg
        params = record.__dict__

        data = { "embeds": 
            [{
                "description": f"## {embed_titles[record.levelname]}\n\n{self.format(record)}",
                "thumbnail": { "url": params.get("user_avatar", None) },
                "footer": { "text": current_time().strftime("%d %B %Y — %H:%M") },
                "color": embed_colors[record.levelname],
            }] }
        files = {}
        for l_file in params.get("files", []):
            if l_file: files[l_file.filename] = l_file.fp

        try:
            webhook_url = getattr(cfg.webhooks_cfg(
                params.get("guild_id", cfg.base_guild_id)),
                log_webhooks[params.get("type", "else")])
            post(webhook_url, data={"payload_json": json.dumps(data)})
            if files:
                post(webhook_url, files=files)

        except exceptions.MissingSchema:
            if not settings.SUPPRESS_WEBHOOK_CONFIGURATION:
                print(
                    "-----------------------------------------------------------------------------------------\n"
                    "Webhooks parameters have not been setted yet.\n "
                    "If you're using API, make sure, that it works correctly and configure parameters using /config.\n "
                    "If you're not using API, then enter parameters manually in 'src/manual_config.py'.\n "
                   "-----------------------------------------------------------------------------------------")

        except KeyError:
            pass

        except Exception as e:
            raise LoggerException(str(e))


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