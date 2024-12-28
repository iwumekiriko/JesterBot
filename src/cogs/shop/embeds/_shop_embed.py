from src.utils.ui import BaseEmbed


class ShopEmbed(BaseEmbed):
    def __init__(
        self, **kwargs
    ) -> None:
        super().__init__(
            title = kwargs.get('title'),
            description = kwargs.get('description'),
            color=0xe74c3c
        )