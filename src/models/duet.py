from datetime import datetime

from .guild import Guild
from .user import User


class Duet:
    def __init__(
        self,
        guild_id: int,
        guild: Guild,
        proposer_id: int,
        proposer: User,
        duo_id: int,
        duo: User,
        together_from: datetime | float
    ) -> None:
        self._guild_id = guild_id
        self._guild = guild
        self._proposer_id = proposer_id
        self._proposer = proposer
        self._duo_id = duo_id
        self._duo = duo
        self._together_from = together_from

    @property
    def guild_id(self) -> int:
        return self._guild_id
    
    @property
    def guild(self) -> Guild:
        return self._guild
    
    @property
    def proposer_id(self) -> int:
        return self._proposer_id
    
    @property
    def proposer(self) -> User:
        return self._proposer
    
    @property
    def duo_id(self) -> int:
        return self._duo_id
    
    @property
    def duo(self) -> User:
        return self._duo
    
    @property
    def together_from(self) -> datetime | float:
        return self._together_from
    
