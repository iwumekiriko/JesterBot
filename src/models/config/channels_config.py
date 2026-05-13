from dataclasses import dataclass

from .base_config import BaseConfig


@dataclass
class ChannelsConfig(BaseConfig):
    general_channel_id: int | None = None
    offtop_channel_id: int | None = None
    nitro_boosting_channel_id: int | None = None
    image_saver_channel_id: int | None = None

    def to_dict(self) -> dict:
        return {
            "guildId": self.guild_id,
            "generalChannelId": self.general_channel_id,
            "offtopChannelId": self.offtop_channel_id,
            "nitroBoostingChannelId": self.nitro_boosting_channel_id,
            "imageSaverChannelId": self.image_saver_channel_id
        }