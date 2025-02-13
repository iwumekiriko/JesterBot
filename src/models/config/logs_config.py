from dataclasses import dataclass

from .base_config import BaseConfig


@dataclass
class LogsConfig(BaseConfig):
    command_interactions_webhook_url: str | None = None
    messages_webhook_url: str | None = None
    tickets_webhook_url: str | None = None
    guild_webhook_url: str | None = None
    members_webhook_url: str | None = None
    voice_webhook_url: str | None = None
    else_webhook_url: str | None = None

    def to_dict(self) -> dict:
        return {
            "guildId": self.guild_id,
            "commandInteractionsWebhookUrl": self.command_interactions_webhook_url,
            "messagesWebhookUrl": self.messages_webhook_url,
            "ticketsWebhookUrl": self.tickets_webhook_url,
            "guildWebhookUrl": self.guild_webhook_url,
            "membersWebhookUrl": self.members_webhook_url,
            "voiceWebhookUrl": self.voice_webhook_url,
            "elseWebhookUrl": self.else_webhook_url
        }
