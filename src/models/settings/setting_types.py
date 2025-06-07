from enum import Enum

from src.localization import get_localizator


_ = get_localizator("settings.types")


class SettingTypes(Enum):
    EXP_DISABLING = 1
    AUTO_QUEST_TAKE = 2
    AUTO_BOOST_EXTEND = 3
    RESTRICT_INTERACTIONS = 4
    RESTRICT_DUET_DISPOSE = 5

    @property
    def translated(self) -> str:
        return _(self.name.lower())
    
    @property
    def translated_desc(self) -> str:
        return _(f"{self.name.lower()}_desc")