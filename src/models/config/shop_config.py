from dataclasses import dataclass

from .base_config import BaseConfig


@dataclass
class ShopConfig(BaseConfig):
    shop_channel_id: int | None = None
    shop_message_id: int | None = None

    def to_dict(self) -> dict:
        return {
            "guildId": self.guild_id,
            "shopChannelId": self.shop_channel_id,
            "shopMessageId": self.shop_message_id,
        }