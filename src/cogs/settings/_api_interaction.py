from src.api_client import APIClient

from src.models.settings import UserSettings, Setting, SettingTypes
from src.utils.enums import Actions
from src.utils._mapping import json_camel_to_snake


async def get_user_settings(guild_id: int, user_id: int) -> UserSettings:
    endpoint = f"UserSettings/{guild_id}/{user_id}"
    async with APIClient() as client:
        response = await client.get(endpoint)
        for i in range(len(response['settings'])):
            response['settings'][i]['type'] = SettingTypes(response['settings'][i]['type'])
            response['settings'][i] = Setting(**json_camel_to_snake(response['settings'][i]))

        return UserSettings(**json_camel_to_snake(response))


async def update_guild_setting(action: Actions, guild_id: int, type: SettingTypes, cost: int) -> None:
    endpoint = f"UserSettings/{guild_id}/update/{type.value}"
    query_params = { "cost": cost }
    async with APIClient() as client:
        match(action):
            case Actions.ADD:
                await client.post(endpoint, query_params=query_params)
            case Actions.REMOVE:
                await client.delete(endpoint)


async def update_setting(guild_id: int, user_id: int, setting: Setting) -> None:
    endpoint = f"UserSettings/{guild_id}/state/{user_id}"
    async with APIClient() as client:
        await client.put(endpoint, body=setting.to_dict())