from dataclasses import dataclass

from .base_config import BaseConfig


@dataclass
class VoiceConfig(BaseConfig):
    custom_voice_creation_channel_id: int | None = None
    custom_voice_category_id: int | None = None
    custom_voice_deletion_time: int | None = None

    def to_dict(self) -> dict:
        return {
            "guildId": self.guild_id,
            "customVoiceCreationChannelId": self.custom_voice_creation_channel_id,
            "customVoiceCategoryId": self.custom_voice_category_id,
            "customVoiceDeletionTime": self.custom_voice_deletion_time,
        }