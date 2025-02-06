from typing import Union
import disnake
from disnake.ext import commands

import disnake.member

from src.bot import JesterBot
from src.logger import get_logger
from ._api_interaction import (
    get_member,
    member_joined,
    member_left
)


logger = get_logger()


class OnGuildCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member) -> None:
        guild_id = member.guild.id
        user_id = member.id
        member_data = await get_member(guild_id, user_id)

        logger.info("Новый участник [<@%d>] заходит на сервер!\n\n \
                    **Кол-во участников на сервере: **%d\n**Id пользователя:** %d",
                     member.id, member.guild.member_count, user_id,
                     extra={ "user_avatar": member.display_avatar.url, "type": "guild" })

        if member_data and not member_data.is_active:
            await member_joined(guild_id, user_id)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member) -> None:
        guild_id = member.guild.id
        user_id = member.id
        member_data = await get_member(guild_id, user_id)
 
        logger.info("Участник [<@%d>] покидает сервер.\n\n\
                    **Кол-во участников на сервере: **%d\n**Id пользователя:** %d\n**Присоединился: **<t:%d:F>",
                     member.id, member.guild.member_count, user_id, member.joined_at.timestamp(), # type: ignore
                     extra={ "user_avatar": member.display_avatar.url, "type": "guild" })

        if member_data and member_data.is_active:
            await member_left(guild_id, user_id)

    @commands.Cog.listener()
    async def on_member_update(
        self,
        before: disnake.Member,
        after: disnake.Member
    ) -> None:
        self._log(before, after)

    @commands.Cog.listener()
    async def on_user_update(
        self,
        before: disnake.User,
        after: disnake.User
    ) -> None:
        self._log(before, after)

    def _log(
        self,
        before: Union[disnake.Member, disnake.User],
        after: Union[disnake.Member, disnake.User]
    ) -> None:
        match before:
            case disnake.Member():
                who = "участника"

            case disnake.User():
                who = "пользователя"

        if (before.display_avatar != after.display_avatar):
            logger.warning("Аватар %s <@%d> был изменён!", who, after.id,
                           extra={ "user_avatar": after.display_avatar.url, "type": "members" })
        
        if (before.display_name != after.display_name):
            logger.warning("Никнейм %s <@%d> был изменён!\n `%s` **->** `%s`",
                           who, after.id, before.display_name, after.display_name,
                           extra={ "user_avatar": after.display_avatar.url, "type": "members" })
