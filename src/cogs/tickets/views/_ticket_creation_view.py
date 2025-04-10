from typing import Callable, Optional
import disnake

from ..embeds import TicketEmbed
from .._modal_forms import (
    bot_modal_form,
    moderator_modal_form,
    support_modal_form
)
from src.localization import get_localizator


_ = get_localizator("tickets")


class TicketCreationView(disnake.ui.View):
    def __init__(
        self
    ) -> None:
        super().__init__(timeout=None)
        self.ticket_options: dict[
            tuple[str, Optional[str]],
            Callable
        ] = {
            (_("support_question"), "❓"): support_modal_form,
            (_("moderation_offense"), "🗡️"): moderator_modal_form,
            (_("bot_issue"), "🤖"): bot_modal_form
        }
        
        self.add_item(OpenTicketSelect(self.ticket_options))

    def create_embed(self) -> disnake.Embed:
        return TicketEmbed(
            title = _("ticket_embed_title"),
            description = _("ticket_embed_description")
        )

class OpenTicketSelect(disnake.ui.Select):
    view: TicketCreationView

    def __init__(self, tickets_options: dict) -> None:
        super().__init__(
            custom_id="open-ticket-select-menu",
            options=[disnake.SelectOption(
                label=name, emoji=emoji)
                for name, emoji in tickets_options])

    async def callback(
        self,
        interaction: disnake.MessageCommandInteraction
    ) -> None:
        name = self.values[0]
        await interaction.message.edit(view=self.view) # type: ignore
        await next((value for key, value in self.view.ticket_options.items()
              if key[0] == name), support_modal_form)(interaction)
        



