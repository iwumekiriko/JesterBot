from typing import Optional
from datetime import datetime

from .user import User
from .guild import Guild


class Member:
    def __init__(
        self,
        guild_id: int,
        guild: Guild,
        user_id: int,
        user: User,
        active: bool = True,
        experience: int = 0,
        exp_multiplier: int = 1,
        coins: int = 0,
        crystals: int = 0,
        message_count: int = 0,
        voice_time: int = 0,
        joined_at: Optional[datetime | str] = None
    ) -> None:
        self._guild_id = guild_id
        self._guild = guild
        self._user_id = user_id
        self._user = user
        self._active = active
        self._experience = experience
        self._exp_multiplier = exp_multiplier
        self._coins = coins
        self._crystals = crystals
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
    def is_active(self) -> bool:
        return self._active

    @is_active.setter
    def is_active(self, active: bool) -> None:
        self._active = active

    @property
    def experience(self) -> int:
        return self._experience

    @experience.setter
    def experience(self, exp: int) -> None:
        self._experience = exp 

    @property
    def exp_multiplier(self) -> int:
        return self._exp_multiplier

    @exp_multiplier.setter
    def exp_multiplier(self, multiplier: int) -> None:
        self._exp_multiplier = multiplier

    @property
    def coins(self) -> int:
        return self._coins

    @coins.setter
    def coins(self, coins: int) -> None:
        self._coins = coins

    @property
    def crystals(self) -> int:
        return self._crystals

    @crystals.setter
    def crystals(self, crystals: int) -> None:
        self._crystals = crystals

    @property
    def message_count(self) -> int:
        return self._message_count

    @message_count.setter
    def message_count(self, mc: int) -> None:
        self._message_count = mc

    @property
    def voice_time(self) -> int:
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
