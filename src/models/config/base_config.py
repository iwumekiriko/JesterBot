from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..guild import Guild

@dataclass
class BaseConfig(ABC):
    guild_id: int
    guild: Guild | None = None

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError
    
    @property
    def short_name(self) -> str:
        return self.__class__.__name__[:-6]