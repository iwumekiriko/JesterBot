from datetime import datetime

from .guild import Guild
from .user import User


class Salary:
    def __init__(
        self,
        guild_id: int,
        guild: Guild,
        user_id: int,
        user: User,
        coins: int,
        date_time: datetime,
        control_id: int,
        staff_id: int,
        is_given: bool,
        type: str
    ) -> None:
        self._guild_id = guild_id
        self._guild = guild
        self._user_id = user_id
        self._user = user
        self._coins = coins
        self._date_time = date_time
        self._control_id = control_id
        self._staff_id = staff_id
        self._is_given = is_given
        self._type = type

    @property
    def guild_id(self) -> int:
        return self.guild_id

    @property
    def guild(self) -> Guild:
        return self.guild

    @property
    def user_id(self) -> int:
        return self.user_id

    @property
    def user(self) -> User:
        return self.user

    @property
    def coins(self) -> int:
        return self._coins

    @property
    def date_time(self) -> datetime:
        return self._date_time

    @property
    def control_id(self) -> int:
        return self._control_id

    @property
    def staff_id(self) -> int:
        return self._staff_id

    @property
    def is_given(self) -> bool:
        return self._is_given

    @property
    def type(self) -> str:
        return self._type