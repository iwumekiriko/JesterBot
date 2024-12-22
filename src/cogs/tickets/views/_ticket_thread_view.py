import disnake

from src.localization import get_localizator
from src.utils.ui import BaseView
from .._api_interaction import ticket_start, ticket_close
from ..embeds import TicketEmbed
from src.utils._convertes import user_avatar
from src.utils._time import current_time


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
        from src.config import cfg
        
        if not interaction.guild:
            return True

        if not isinstance(member := interaction.user, disnake.Member):
            return False
        
        roles_cfg = cfg.roles_cfg(interaction.guild_id) # type: ignore
        roles = [
            roles_cfg.developer_role_id,
            roles_cfg.moderator_role_id,
            roles_cfg.support_role_id
        ]
        
        if not (any(role.id in roles for role in member.roles)):
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
        from src.config import cfg

        data = await solution_modal_form(interaction)
        if len(data) < 2:
            return

        inter: disnake.ModalInteraction = data[0]

        await inter.response.defer(with_message=False)
        ticket = await ticket_close(interaction.channel.id, data[1])

        if not ticket.moderator_id:
            await inter.followup.send(_("close_ticket_button_error"),
                                               ephemeral=True)
            return

        self.disabled = True
        await inter.message.edit( # type: ignore
            embed=TicketEmbed(
                description=_("ticket_thread_embed_desc",
                               user_id=ticket.user_id,
                               desc=ticket.description_problem))
                .set_footer(text=_("ticket_closed_status"))
                .add_field(name=_("ticket_solution"), value=f"```{ticket.solution}```", inline=False)
                .set_thumbnail(user_avatar(user_id=ticket.user_id)), # type: ignore
            view=self.view
        )

        await inter.channel.send(
            content=f"<@{ticket.user_id}>",
            embed=TicketEmbed(
                title=_("ticket_thread_end_embed_title"),
                description=_("ticket_thread_end_embed_desc", 
                              moderator_id=ticket.moderator_id,
                              solution=ticket.solution))
                .set_thumbnail(user_avatar(user_id=ticket.moderator_id)) # type: ignore
        )

        report_channel_id = cfg.tickets_cfg(inter.guild_id).ticket_report_channel_id # type: ignore
        if report_channel_id and inter.guild:
            rep_channel = inter.guild.get_channel(report_channel_id)
            await rep_channel.send( # type: ignore
                embed=TicketEmbed(
                    title = _("ticket_report_embed_title"),
                    description = _("ticket_report_embed_desc",
                                    user_id=ticket.user_id,
                                    moderator_id=ticket.moderator_id,
                                    problem=ticket.description_problem,
                                    solution=ticket.solution,
                                    ticket_url=inter.message.jump_url)) # type: ignore
                    .set_thumbnail(user_avatar(user_id=ticket.moderator_id)) # type: ignore
                    .set_footer(text=current_time().strftime("%d %B %Y — %H:%M"))
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
                                        user_id=ticket.user_id,
                                        moderator_id=interaction.user.id))
        await interaction.response.send_message(
            _("ticket_start_instruction"), ephemeral=True)
