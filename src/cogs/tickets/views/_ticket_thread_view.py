import disnake

from src.localization import get_localizator
from src.utils._views import BaseView
from src._config import SUPPORT_ROLE_ID, MODERATOR_ROLE_ID, DEVELOPER_ROLE_ID
from .._api_interaction import ticket_start, ticket_close
from src.utils._embeds import TicketEmbed
from src.utils._convertes import user_avatar


_ = get_localizator("tickets")


class TicketThreadView(BaseView):
    def __init__(self) -> None:
        super().__init__(timeout=None)

        self.add_item(StartTicketButton())
        self.add_item(ApproveTicketButton())

    async def interaction_check(
        self,
        interaction: disnake.MessageCommandInteraction
    ) -> bool:
        if not interaction.guild:
            return True

        if not isinstance(member := interaction.user, disnake.Member):
            return False

        if not (any(role.id in {
            SUPPORT_ROLE_ID,
            DEVELOPER_ROLE_ID,
            MODERATOR_ROLE_ID
        } for role in member.roles)):
            await interaction.response.send_message(
                _("approve_ticket_button_error"), ephemeral=True)
            return False
        
        return True


class ApproveTicketButton(disnake.ui.Button):
    view: TicketThreadView

    def __init__(self) -> None:
        super().__init__(
            custom_id="approve-ticket-button",
            label=_("approve_ticket_button"),
            style=disnake.ButtonStyle.green
        )

    async def callback(
        self,
        interaction: disnake.MessageCommandInteraction
    ) -> None:
        from .._modal_forms import solution_modal_form
        data = await solution_modal_form(interaction)
        if len(data) < 2:
            return

        inter: disnake.ModalInteraction = data[0]

        await inter.response.defer(with_message=False)
        ticket = await ticket_close(interaction.channel.id, data[1])

        self.disabled = True
        await inter.message.edit( # type: ignore
            embed=TicketEmbed(
                description=_("ticket_thread_embed_desc",
                               user_id=ticket.user_id,
                               desc=ticket.description_problem))
                .set_footer(text=_("ticket_closed_status"))
                .add_field(name="Решение проблемы: ", value=f"```{ticket.solution}```", inline=False)
                .set_thumbnail(user_avatar(user_id=ticket.user_id)), # type: ignore
            view=self.view
        )

        if isinstance(thread := interaction.channel, disnake.Thread):
            await thread.edit(locked=True, archived=True)


class StartTicketButton(disnake.ui.Button):
    view: TicketThreadView

    def __init__(self) -> None:
        super().__init__(
            custom_id="start-ticket-button",
            label=_("start_ticket_button"),
            style=disnake.ButtonStyle.gray
        )

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        ticket = await ticket_start(interaction.channel.id, interaction.user.id)
        
        self.disabled = True
        await interaction.message.edit( # type: ignore
            embed=TicketEmbed(
                description=_("ticket_thread_embed_desc",
                               user_id=ticket.user_id,
                               desc=ticket.description_problem))
                .set_footer(text=_("ticket_active_status"))
                .set_thumbnail(user_avatar(user_id=ticket.user_id)), # type: ignore
            view=self.view
        ) 
        
        await interaction.channel.send(_("ticket_started",
                                        moderator_id=interaction.user.id))
        await interaction.response.send_message(
            _("ticket_start_instruction"), ephemeral=True)
