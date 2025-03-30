from abc import ABC, abstractmethod
from typing import Dict
from uuid import UUID
from disnake import MessageCommandInteraction, Embed, Guild, Member

from src.utils._events import CustomEvents
from .._api_interaction import get_lootbox_data, save_lootbox_data
from src.models.lootboxes import LootboxTypes, LootboxUserData


class BaseLootbox(ABC):
    def __init__(
        self,
        interaction: MessageCommandInteraction,
        uuid: UUID
    ) -> None:
        self._interaction = interaction
        self._uuid = uuid
        self._guild: Guild = interaction.guild # type: ignore
        self._user: Member = interaction.user # type: ignore

    @abstractmethod
    async def get_prize(cls, count: int) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def create_embed(
        cls, guild: Guild, user: Member
    ) -> Embed:
        raise NotImplementedError

    def items_received(
        self, items
    ) -> None:
        from src.bot import bot

        bot.dispatch(CustomEvents.LOOTBOXES_ITEM_RECEIVED,
                        items=items, uuid=self._uuid)

    @property
    def type_(self) -> str:
        return self.__class__.__name__[:-7]

    async def _get_user_data(self, type: LootboxTypes) -> LootboxUserData:
        return await get_lootbox_data(
            self._guild.id,
            self._user.id,
            type=type
        )

    async def _save_user_data(self, data: LootboxUserData) -> None:
        await save_lootbox_data(data=data)
