from dataclasses import dataclass

from .base_config import BaseConfig


@dataclass
class ShopConfig(BaseConfig):
    guild_id: int
    shop_channel_id: int | None = None
    shop_message_id: int | None = None

    def to_dict(self) -> dict:
        return {
            "guildId": self.guild_id,
            "ticketChannelId": self.shop_channel_id,
            "ticketMessageId": self.shop_message_id,
        }