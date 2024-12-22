import disnake

from src.localization import get_localizator


_ = get_localizator()


class BaseView(disnake.ui.View):
    def __init__(
            self, *, timeout: float | None = 180
        ) -> None:
        super().__init__(timeout=timeout)
        self.author: disnake.Member | disnake.User
        self.message: disnake.Message

    async def interaction_check(
        self,
        interaction: disnake.MessageInteraction
    ) -> bool:
        if not hasattr(self, "author"):
            return True
        
        if not self.author.id == interaction.user.id:
            await interaction.response.send_message(
                _("not_an_interaction_author_err"),
                ephemeral=True
            )
            return False
        return True
    
    async def on_timeout(self) -> None:
        if not hasattr(self, "message"):
            return
        
        for item in self.children:
            item.disabled = True # type: ignore

        await self.message.edit(view=self)

    async def start(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        await self._response(interaction)
        self.message = await interaction.original_message()
        self.author = interaction.author

    async def _response(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        await interaction.response.send_message(view=self)