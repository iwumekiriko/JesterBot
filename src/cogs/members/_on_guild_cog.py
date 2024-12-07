import disnake
from disnake.ext import commands

import disnake.member

from src.bot import JesterBot
from src.logger import get_logger
from ._api_interaction import get_member, member_joined, member_left


logger = get_logger()


class OnGuildCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member) -> None:
        guild_id = member.guild.id
        member_id = member.id
        member_data = await get_member(member_id, guild_id)
        logger.info("Новый участник [<@%d>] зашел на сервер!\n\n**Кол-во участников на сервере: **%d\n**Id пользователя:** %d",
                     member.id, member.guild.member_count, member_id,
                     extra={ "user_avatar": member.display_avatar.url, "type": "guild" })

        if member_data and not member_data.is_active:
            await member_joined(member_data)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member) -> None:
        guild_id = member.guild.id
        member_id = member.id
        member_data = await get_member(member_id, guild_id)
 
        logger.info("Участник [<@%d>] покинул сервер.\n\n**Кол-во участников на сервере: **%d\n**Id пользователя:** %d\n**Присоединился: **<t:%d:F>",
                     member.id, member.guild.member_count, member_id, member.joined_at.timestamp(), # type: ignore
                     extra={ "user_avatar": member.display_avatar.url, "type": "guild" })

        if member_data and member_data.is_active:
            await member_left(member_data)

    @commands.Cog.listener()
    async def on_member_update(
        self,
        before: disnake.Member,
        after: disnake.Member
    ) -> None:
        if before.display_avatar != after.display_avatar:
            logger.warning("Пользователь <@%d> изменил аватар!", after.id,
                           extra={ "user_avatar": after.display_avatar.url, "type": "members" })
        
        if before.nick != after.nick:
            before_nick = before.nick or before.global_name
            after_nick = after.nick or after.global_name
            logger.warning("Пользователь <@%d> изменил никнейм!\n `%s` **->** `%s`",
                           after.id, before_nick, after_nick,
                           extra={ "user_avatar": after.display_avatar.url, "type": "members" })