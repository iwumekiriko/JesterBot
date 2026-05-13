from dataclasses import dataclass
from typing import Optional
from .log_level import LogLevel


@dataclass
class Log:
    guild_id: int
    level: LogLevel
    message: str
    category: str
    avatar_url: Optional[str]
    images_urls: Optional[list[str]]
    files_urls: Optional[list[str]]

    def to_dict(self) -> dict:
        return {
            "guildId": self.guild_id,
            "level": self.level.value,
            "message": self.message,
            "category": self.category,
            "avatarUrl": self.avatar_url,
            "imagesUrls": self.images_urls,
            "filesUrls": self.files_urls
        }