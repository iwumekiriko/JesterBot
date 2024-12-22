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
        logger.info("Новый участник [<@%d>] заходит на сервер!\n\n**Кол-во участников на сервере: **%d\n**Id пользователя:** %d",
                     member.id, member.guild.member_count, user_id,
                     extra={ "user_avatar": member.display_avatar.url, "type": "guild" })

        if member_data and not member_data.is_active:
            await member_joined(guild_id, user_id)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member) -> None:
        guild_id = member.guild.id
        user_id = member.id
        member_data = await get_member(guild_id, user_id,)
 
        logger.info("Участник [<@%d>] покидает сервер.\n\n**Кол-во участников на сервере: **%d\n**Id пользователя:** %d\n**Присоединился: **<t:%d:F>",
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
        if before.display_avatar != after.display_avatar or before.display_avatar != after.avatar:
            logger.warning("Пользователь <@%d> изменяет аватар!", after.id,
                           extra={ "user_avatar": after.display_avatar.url, "type": "members" })
        
        if before.display_name != after.display_name:
            logger.warning("Пользователь <@%d> изменяет никнейм!\n `%s` **->** `%s`",
                           after.id, before.display_name, after.display_name,
                           extra={ "user_avatar": after.display_avatar.url, "type": "members" })