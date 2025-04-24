from src.utils.ui import BaseEmbed
from src.customisation import BASE_QUESTS_COLOR


class QuestsEmbed(BaseEmbed):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.color = BASE_QUESTS_COLOR