import disnake
from typing import Dict, List, Optional, Tuple

from src.utils.ui import Paginator, BaseEmbed, State, SuccessEmbed
from src.models.quests import Quest, QuestTypes
from src.utils._cards import quests_card
from .._api_interaction import accept_quest

from src.localization import get_localizator


_ = get_localizator("quests.views")


class QuestsPaginator(Paginator[Quest]):
    def __init__(
        self,
        items: List[Quest],
        *,
        on_board: bool = True,
        items_per_page: int = 1,
        timeout: Optional[float] = 300
    ) -> None:
        self._all_quests = items
        super().__init__(
            items=items,
            items_per_page=items_per_page,
            timeout=timeout
        )
        self.__updateable = []
        self.type_options = {
            (_("quests-views-daily_category"), "🏕️"): QuestTypes.DAILY,
            (_("quests-views-weekly_category"), "🏜️"): QuestTypes.WEEKLY,
            (_("quests-views-event_category"), "🏖️"): QuestTypes.EVENT
        }
        self._by_types: Dict[QuestTypes, List[Quest]] = {}
        if on_board:
            accept_button = AcceptQuestButton()
            self.add_item(accept_button)
            self.__updateable.append(accept_button)
        else:
            quests_select = QuestsSelect(self.type_options)
            self.add_item(quests_select)
            for quest in self._all_quests:
                quests = self._by_types.setdefault(quest.type, [])
                quests.append(quest)

            self.select_quests_by_type(list(self.type_options.values())[0])

        self._update_components()

    def create_embed(self) -> disnake.Embed:
        if not self._all_quests:
            return BaseEmbed(description=_("quests-views-empty-quest-desc"))
        if not self.page_items:
            return BaseEmbed(description=_("quests-views-empty-quest-category-desc"))
        return quests_card(self.first_item) # type: ignore

    async def page_button_callback(
        self,
        interaction: disnake.MessageInteraction 
                     | disnake.ModalInteraction
    ) -> None:
        self._update_components()
        await interaction.response.edit_message(
            embed=self.create_embed(),
            view=self
        )

    def to_state(
        self, kwargs: Optional[dict] = None
    ) -> State:
        return State(
            view = self,
            embed = self.create_embed(),
            kwargs = kwargs
        )

    async def _response(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        await interaction.response.send_message(
            embed=self.create_embed(),
            view=self,
            ephemeral=True
        )

    async def update_view(self) -> None:
        self._update_components()
        await self.message.edit(
            view=self,
            embed=self.create_embed()
        )

    def _update_components(self):
        for component in self.__updateable:
            component.update()

    def select_quests_by_type(self, type: QuestTypes) -> None:
        self.change_all(self._by_types.get(type, []))


class AcceptQuestButton(disnake.ui.Button):
    view: QuestsPaginator

    def __init__(self) -> None:
        super().__init__(
            label=_("quests-views-accept_button_label"),
            style=disnake.ButtonStyle.green
        )

    def update(self) -> None:
        if not (fc := self.view.first_item):
            self.disabled = True
            return

        self.disabled = fc.accepted_by_user

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        quest = self.view.first_item
        if not quest:
            return

        await accept_quest(quest.guild_id, interaction.user.id, quest.id)
        quest.accepted_by_user = True
        await self.view.update_view()
        # await interaction.followup.send(
        #     embed=SuccessEmbed(success_msg=_("quests-views-accept_button_success")),
        #     ephemeral=True
        # )


class QuestsSelect(disnake.ui.Select):
    view: QuestsPaginator

    def __init__(self, type_options: Dict[Tuple[str, str], QuestTypes]):
        super().__init__(
            options=[disnake.SelectOption(
                label=quest_type, emoji=emoji
            ) for quest_type, emoji in type_options]
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        view = self.view

        name = self.values[0]
        type_option = next(
            (value for key, value in 
             view.type_options.items() if key[0] == name))

        await interaction.response.defer(with_message=False)
        view.select_quests_by_type(type_option)
        await view.update_view()
