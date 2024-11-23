import disnake

from .views._ticket_thread_view import TicketThreadView
from .classes._thread_classification import ThreadClassification
from src.models import Ticket
from ._api_interaction import ticket_create
from src.utils._embeds import TicketEmbed
from src.localization import get_localizator


_ = get_localizator("tickets")


async def _ticket_thread_create(
    interaction: disnake.ModalInteraction,
    type: ThreadClassification
) -> disnake.Thread:
    return await interaction.channel.create_thread( # type: ignore
        name=f"{type.name} ticket",
        type=disnake.ChannelType.private_thread,
        invitable=True,
        auto_archive_duration=10080
    )


async def ticket(data: list, type: ThreadClassification) -> None:
    if not data[1]:
        return

    inter: disnake.ModalInteraction = data[0]
    await inter.response.defer(with_message=False)

    thread = await _ticket_thread_create(inter, type)
    ticket = Ticket(
        id=thread.id,
        description_problem=data[1],
        additional_info=data[2] if len(data) > 2 else None,
        user_id=inter.user.id,
        type_problem=type.name.lower()
    )
    await ticket_create(ticket)
    await _send_ticket(thread, type, ticket)


async def _send_ticket(
        thread: disnake.Thread,
        type: ThreadClassification,
        ticket: Ticket
) -> None:
    message = await thread.send(
            content=f"<@{ticket.user_id}> <@&{type.value}>",
            embed = TicketEmbed(
                title=_("ticket_thread_embed_title"),
                description=_("ticket_thread_embed_desc",
                               user_id=ticket.user_id,
                               desc=ticket.description_problem,
                               add_info=ticket.additional_info or _("_no"))
            ),
            view=TicketThreadView()
        )
    await message.pin()