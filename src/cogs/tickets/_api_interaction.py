import aiohttp
import json

from src.models import Ticket
from src.logger import get_logger
from src.utils._mapping import json_camel_to_snake
from src._config import PATH_TO_API
from src.utils._exceptions import BaseException


logger = get_logger()


async def ticket_create(ticket: Ticket) -> None:
    async with aiohttp.ClientSession() as session:
        data = json.dumps(ticket.to_create())
        headers = {'Content-Type': 'application/json'}
        async with session.post(
            PATH_TO_API + "Tickets/Create",
            ssl=False, data=data, headers=headers
        ) as response:
                if response.status == 200:
                    logger.info("ticket created successfully")
                else:
                    error_message = await response.text()
                    raise BaseException("Tickets API is not responding."
                                    f"Status code: {response.status}. Error: {error_message}")
                

async def _ticket_get(ticket_id: int) -> Ticket:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            PATH_TO_API + f"Tickets/Get?id={ticket_id}", ssl=False
        ) as response:
            if response.status == 200:
                json_data = await response.json()
                return Ticket(**json_camel_to_snake(json_data))
            else:
                error_message = await response.text()
                raise BaseException("Tickets API is not responding."
                                f"Status code: {response.status}. Error: {error_message}")
            

async def ticket_start(ticket_id: int, moderator_id: int) -> str | None:
    ticket = await _ticket_get(ticket_id)
    ticket.moderator_id = moderator_id

    data = json.dumps(ticket.to_start())
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + f"Tickets/Start?id={ticket_id}",
            ssl=False, data=data, headers=headers
        ) as response:
            if response.status == 200:
                logger.info("ticket updated successfully")
                message = ""
            else:
                error_message = await response.text()
                raise BaseException("Tickets API is not responding."
                                f"Status code: {response.status}. Error: {error_message}")


async def ticket_close(ticket_id: int, solution: str) -> None:
    ticket = await _ticket_get(ticket_id)
    ticket.solution = solution

    data = json.dumps(ticket.to_close())
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + f"Tickets/Close?id={ticket_id}",
            ssl=False, data=data, headers=headers
        ) as response:
            if response.status == 200:
                logger.info("ticket closed successfully")
            else:
                error_message = await response.text()
                raise BaseException("Tickets API is not responding."
                                f"Status code: {response.status}. Error: {error_message}")


            

