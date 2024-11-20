from enum import Enum

from src.localization import get_localizator


_ = get_localizator("interactions")


class InteractionChoices(str, Enum):
    KISS = "kiss"
    HUG = "hug"
    PAT = "pat"
    HIT = "hit"

    @property
    def translated_name(self) -> str:
        return _(self.value + '_choice')


class InteractionType(str, Enum):
    CAT = "cat"
    ANIME = "anime"

    @property
    def translated_name(self) -> str:
        return _(self.value + '_choice')