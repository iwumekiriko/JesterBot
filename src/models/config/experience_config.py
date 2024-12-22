from dataclasses import dataclass

from .base_config import BaseConfig


@dataclass
class ExperienceConfig(BaseConfig):
    exp_for_message: int | None = None
    exp_for_voice_minute: int | None = None

    def to_dict(self) -> dict:
        return {
            "guildId": self.guild_id,
            "expForMessage": self.exp_for_message,
            "expForVoiceMinute": self.exp_for_voice_minute
        }