import aiohttp
from disnake.ext import commands
import random

from ._interactions_choice import InteractionChoices, InteractionType
from src._config import TENOR_API_KEY


async def get_gif(
    query: InteractionChoices,
    type: InteractionType,
    limit: int = 30
) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            'https://tenor.googleapis.com/v2/search?' 
            f'q={type}%20{query}&'
            f'key={TENOR_API_KEY}&'
            'contentfilter=medium&'
            'media_filter=minimal&'
            f'limit={limit}'
        ) as response:
            if response.status == 200:
                json_response = await response.json()
                return json_response['results'][random.randint(0, limit-1)]['media_formats']['gif']['url']
            else:
                raise commands.BadArgument("API is not responding!")