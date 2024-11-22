import aiohttp
import random

from ._interactions_choice import InteractionChoices, InteractionType
from src._config import TENOR_API_KEY
from src.utils._exceptions import BaseException


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
                error_message = await response.text()
                raise BaseException("Tenor API is not responding."
                                f"Status code: {response.status}. Error: {error_message}")