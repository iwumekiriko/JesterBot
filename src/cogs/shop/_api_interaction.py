import aiohttp
from src.settings import PATH_TO_API

async def get_roles(
    guild_id: int
) -> dict:
    return {
        1309328136302886992:1000000,
        1309329395336351767:9999,
        1309329505059340398:10
    }

async def zabral_dengi(guild_id: int, user_id: int, amount: int) -> str | None:
    async with aiohttp.ClientSession() as session:
        async with session.put(
            PATH_TO_API + f"Members/{guild_id}/{user_id}/spending?coins={amount}", ssl=False
        ) as response:
            if response.status == 404:
                return "Недостаточно средств :money_with_wings:"
            if not response.status == 200:
                error_message = await response.text()
                raise BaseException("Members API [OnGuild] is not responding. "
                                    f"Status code: {response.status}. Error: {error_message}")
