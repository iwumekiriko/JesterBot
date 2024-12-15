from dataclasses import dataclass

from .base_config import BaseConfig


@dataclass
class ChannelsConfig(BaseConfig):
    guild_id: int
    general_channel_id: int | None = None
    offtop_channel_id: int | None = None

    def to_dict(self) -> dict:
        return {
            "guildId": self.guild_id,
            "generalChannelId": self.general_channel_id,
            "offtopChannelId": self.offtop_channel_id,
        }