from typing import Optional
from datetime import datetime


class Member():
    def __init__(
        self,
        guild_id: int,
        user_id: int,
        active: Optional[bool] = None,
        experience: Optional[int] = None,
        coins: Optional[int] = None,
        message_count: Optional[int] = None,
        voice_time: Optional[int] = None,
        joined_at: Optional[datetime | str] = None
    ) -> None:
        self._guild_id = guild_id
        self._user_id = user_id
        self._active = active
        self._experience = experience
        self._coins = coins
        self._message_count = message_count
        self._voice_time = voice_time
        self._joined_at = joined_at

    @property
    def guild_id(self) -> int:
        return self._guild_id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def is_active(self) -> Optional[bool]:
        return self._active
    
    @is_active.setter
    def is_active(self, active: bool) -> None:
        self._active = active

    @property
    def experience(self) -> Optional[int]:
        return self._experience

    @property
    def coins(self) -> Optional[int]:
        return self._coins

    @property
    def message_count(self) -> Optional[int]:
        return self._message_count

    @property
    def voice_time(self) -> Optional[int]:
        return self._voice_time
    
    @property
    def joined_at(self) -> Optional[datetime | str]:
        return self._joined_at
    
    def to_on_guild(self) -> dict:
        return {
            "userId": self._user_id,
            "guildId": self._guild_id,
            "active": self._active
        }
    