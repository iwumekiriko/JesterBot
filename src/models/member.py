from typing import Optional
from datetime import datetime

from .user import User
from .guild import Guild


class Member():
    def __init__(
        self,
        user_id: int,
        user: User,
        guild_id: int,
        guild: Guild,
        active: Optional[bool] = None,
        experience: Optional[int] = None,
        exp_multiplier: Optional[int] = None,
        coins: Optional[int] = None,
        message_count: Optional[int] = None,
        voice_time: Optional[int] = None,
        joined_at: Optional[datetime | str] = None
    ) -> None:
        self._user_id = user_id
        self._user = user
        self._guild_id = guild_id
        self._guild = guild
        self._active = active
        self._experience = experience
        self._exp_multiplier = exp_multiplier
        self._coins = coins
        self._message_count = message_count
        self._voice_time = voice_time
        self._joined_at = joined_at

    @property
    def guild_id(self) -> int:
        return self._guild_id

    @property
    def guild(self) -> Guild:
        return self._guild

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def user(self) -> User:
        return self._user

    @property
    def is_active(self) -> Optional[bool]:
        return self._active
    
    @is_active.setter
    def is_active(self, active: bool) -> None:
        self._active = active

    @property
    def experience(self) -> Optional[int]:
        return self._experience
    
    @experience.setter
    def experience(self, exp: int) -> None:
        self._experience = exp 

    @property
    def exp_multiplier(self) -> Optional[int]:
        return self._exp_multiplier
    
    @exp_multiplier.setter
    def exp_multiplier(self, multiplier: int) -> None:
        self._exp_multiplier = multiplier

    @property
    def coins(self) -> Optional[int]:
        return self._coins

    @coins.setter
    def coins(self, coins: int) -> None:
        self._coins = coins

    @property
    def message_count(self) -> Optional[int]:
        return self._message_count
    
    @message_count.setter
    def message_count(self, mc: int) -> None:
        self._message_count = mc

    @property
    def voice_time(self) -> Optional[int]:
        return self._voice_time
    
    @voice_time.setter
    def voice_time(self, vt: int) -> None:
        self._voice_time = vt
    
    @property
    def joined_at(self) -> Optional[datetime | str]:
        return self._joined_at
    
    def to_on_guild(self) -> dict:
        return {
            "userId": self._user_id,
            "guildId": self._guild_id,
            "active": self._active
        }
    
    def to_update(self) -> dict:
        return {
            "userId": self._user_id,
            "guildId": self._guild_id,
            "experience": self._experience,
            "expMultiplier": self._exp_multiplier,
            "coins": self._coins,
            "messageCount": self._message_count,
            "voiceTime": self._voice_time
        }