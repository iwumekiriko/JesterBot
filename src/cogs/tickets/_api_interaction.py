from src.models import Ticket
from src.models.config import TicketsConfig
from src.logger import get_logger
from src.utils._mapping import json_camel_to_snake
from src.utils._converters import user_avatar
from src._api_interaction import set_cfg
from src.config import cfg as config
from src.api_client import APIClient


logger = get_logger()


async def ticket_create(ticket: Ticket) -> None:
    endpoint = "Tickets"
    data = ticket.to_create()
    async with APIClient() as client:
        await client.post(
            endpoint,
            body=data
        )
        logger.info("Пользователь <@%d> создаёт тикет [<#%d>]",
                    ticket.user_id, ticket.id,
                    extra={
                        "user_avatar": user_avatar(ticket.user_id), # type: ignore
                        "type": "ticket",
                        "guild_id": ticket.guild_id
                    })


async def _ticket_get(ticket_id: int) -> Ticket:
    endpoint = f"Tickets/{ticket_id}"
    async with APIClient() as client:
        response = await client.get(endpoint)
        return Ticket(**json_camel_to_snake(response)) # type: ignore


async def ticket_start(ticket_id: int, moderator_id: int) -> Ticket:
    ticket = await _ticket_get(ticket_id)
    ticket.moderator_id = moderator_id

    data = ticket.to_start()
    endpoint = f"Tickets/start"
    async with APIClient() as client:
        await client.put(
            endpoint,
            body=data
        )
        logger.info("Модератор <@%d> принимает тикет [<#%d>]",
                    ticket.moderator_id, ticket.id,
                    extra={
                        "user_avatar": user_avatar(ticket.moderator_id), # type: ignore
                        "type": "ticket",
                        "guild_id": ticket.guild_id
                    }) 
        return ticket


async def ticket_close(ticket_id: int, solution: str) -> Ticket:
    ticket = await _ticket_get(ticket_id)
    ticket.solution = solution

    data = ticket.to_close()
    endpoint = f"Tickets/close"
    async with APIClient() as client:
        await client.put(
            endpoint,
            body=data
        )
        logger.info("Модератор <@%d> закрывает тикет [<#%d>]",
                    ticket.moderator_id, ticket.id,
                    extra={
                        "user_avatar": user_avatar(ticket.moderator_id), # type: ignore
                        "type": "ticket",
                        "guild_id": ticket.guild_id
                    })
        return ticket


async def set_ticket_message(
    guild_id: int,
    ticket_message_id: int
) -> None:
    cfg = TicketsConfig(
            guild_id=guild_id,
            ticket_message_id=ticket_message_id)
    config.set_(cfg)
    await set_cfg(cfg)
