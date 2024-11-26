import aiohttp
import json

from src.models import Ticket
from src.logger import get_logger
from src.utils._mapping import json_camel_to_snake
from src._config import PATH_TO_API
from src.utils._exceptions import BaseException
from src.utils._convertes import user_avatar


logger = get_logger()


async def ticket_create(ticket: Ticket) -> None:
    async with aiohttp.ClientSession() as session:
        data = json.dumps(ticket.to_create())
        headers = {'Content-Type': 'application/json'}
        async with session.post(
            PATH_TO_API + "Tickets/Create",
            data=data, headers=headers, ssl=False
        ) as response:
                if response.status == 200:
                    logger.info("Пользователь <@%d> создал тикет [<#%d>]\n\n**Метка: **{ %s }\n**Проблема: **\n```%s```",
                                 ticket.user_id, ticket.id, ticket.type_problem, ticket.description_problem,
                                 extra={"user_avatar": user_avatar(ticket.user_id), "type": "ticket"}) # type: ignore
                else:
                    error_message = await response.text()
                    raise BaseException("Tickets API [Create] is not responding. "
                                        f"Status code: {response.status}. Error: {error_message}")
                

async def _ticket_get(ticket_id: int) -> Ticket:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            PATH_TO_API + f"Tickets/Get/{ticket_id}", ssl=False
        ) as response:
            if response.status == 200:
                json_data = await response.json()
                return Ticket(**json_camel_to_snake(json_data))
            else:
                error_message = await response.text()
                raise BaseException("Tickets API [Get] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")
            

async def ticket_start(ticket_id: int, moderator_id: int) -> Ticket:
    ticket = await _ticket_get(ticket_id)
    ticket.moderator_id = moderator_id

    data = json.dumps(ticket.to_start())
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + f"Tickets/Start",
            data=data, headers=headers, ssl=False
        ) as response:
            if response.status == 200:
                logger.info("Модератор <@%d> принял тикет [<#%d>]", ticket.moderator_id, ticket.id,
                             extra={"user_avatar": user_avatar(ticket.moderator_id), "type": "ticket"}) # type: ignore
                return ticket
            else:
                error_message = await response.text()
                raise BaseException("Tickets API [Start] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")


async def ticket_close(ticket_id: int, solution: str) -> Ticket:
    ticket = await _ticket_get(ticket_id)
    ticket.solution = solution

    data = json.dumps(ticket.to_close())
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + f"Tickets/Close",
            data=data, headers=headers, ssl=False
        ) as response:
            if response.status == 200:
                logger.info("Модератор <@%d> закрыл тикет [<#%d>]\n\n**Решение: **\n```%s```",
                            ticket.moderator_id, ticket.id, ticket.solution,
                            extra={"user_avatar": user_avatar(ticket.moderator_id), "type": "ticket"}) # type: ignore
                return ticket
            else:
                error_message = await response.text()
                raise BaseException("Tickets API [Close] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")


            

