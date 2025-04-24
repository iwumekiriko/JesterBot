from dataclasses import dataclass

from .base_config import BaseConfig


@dataclass
class QuestsConfig(BaseConfig):
    quests_channel_id: int | None = None
    quests_message_id: int | None = None

    def to_dict(self) -> dict:
        return {
            "guildId": self.guild_id,
            "questsChannelId": self.quests_channel_id,
            "questsMessageId": self.quests_message_id
        }
