from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class BaseConfig(ABC):
    guild_id: int

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError
    
    @property
    def short_name(self) -> str:
        return self.__class__.__name__[:-6]