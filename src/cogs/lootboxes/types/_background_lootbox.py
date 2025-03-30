import random
import asyncio
from enum import Enum
from uuid import UUID

from disnake import MessageCommandInteraction, Embed
from disnake.errors import NotFound

from ._base_lootbox import BaseLootbox
from src.localization import get_localizator
from src.utils.ui import BaseEmbed


_ = get_localizator("lootboxes-backgrounds")


GIF_ANIMATION_TIME = 5


class BackgroundsPrizes(str, Enum):
    COINS = _("lootboxes-backgrounds_coins_prize")
    BACKGROUND1 = _("lootboxes-backgrounds_background1_prize")
    BACKGROUND2 = _("lootboxes-backgrounds_background2_prize")
    BACKGROUND3 = _("lootboxes-backgrounds_background3_prize")

    @staticmethod
    def chances() -> dict[int, str]:
        return {
            50: BackgroundsPrizes.COINS,
            36: BackgroundsPrizes.BACKGROUND1,
            12: BackgroundsPrizes.BACKGROUND2,
            2: BackgroundsPrizes.BACKGROUND3,
        }


class BackgroundsLootbox(BaseLootbox):
    def __init__(
        self,
        interaction: MessageCommandInteraction,
        uuid: UUID
    ) -> None:
        super().__init__(interaction, uuid)

    async def get_prize(self) -> None:
        inter = self._interaction
        prize = self._get_roles_prizes()
        p_gif = await get_prize_gif(self._guild.id, self.type_, prize) # type: ignore 
        await self._prize_handler(inter, prize, p_gif)   

    @staticmethod
    def create_embed() -> Embed:
        return BaseEmbed(description=_("lootboxes-backgrounds_embed_desc"))

    def _get_roles_prizes(self) -> str:
        chances = BackgroundsPrizes.chances()
        return random.choices(
            population=list(chances.values()),
            weights=list(chances.keys()),
            k=1)[0]

    async def _prize_handler(
        self,
        inter: MessageCommandInteraction,
        prize: str,
        p_gif: str
    ) -> None:
        match prize:

            case BackgroundsPrizes.COINS as coins:
                prize_value = coins.value

            case BackgroundsPrizes.BACKGROUND1 as background1:
                prize_value = background1.value
            
            case BackgroundsPrizes.BACKGROUND2 as background2:
                prize_value = background2.value

            case BackgroundsPrizes.BACKGROUND3 as background3:
                prize_value = background3.value

            case _:
                prize_value = "error"

        try:
            await inter.edit_original_message(embed=BaseEmbed().set_image(p_gif))
            await asyncio.sleep(GIF_ANIMATION_TIME)
            await inter.edit_original_message(embed=BaseEmbed(description=prize_value))

        except NotFound:
            pass