from src.utils.ui import BaseEmbed
from src.customisation import BASE_SHOP_COLOR


class ShopEmbed(BaseEmbed):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.color = BASE_SHOP_COLOR