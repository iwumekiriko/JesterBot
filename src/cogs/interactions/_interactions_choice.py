from enum import Enum

from src.localization import get_localizator


_ = get_localizator("interactions.common")


class InteractionActions(Enum):
    KISS = 1
    HUG = 2
    PAT = 3
    HIT = 4

    @property
    def translated_name(self) -> str:
        return _(self.name.lower() + '_choice')


class InteractionTypes(Enum):
    CAT = 1
    ANIME = 2
    BUNNY = 3

    @property
    def translated_name(self) -> str:
        return _(self.name.lower() + '_choice')