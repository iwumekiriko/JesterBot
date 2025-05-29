from typing import Union
from enum import Enum

import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.logger import get_logger
from src.localization import get_localizator

from .._api_interaction import (
    get_member,
    member_joined,
    member_left
)
from src.utils._events import CustomEvents
from src.settings import API_REQUIRED, BASE_GUILD_ID
from .._utils import check_for_mod_actions
from ..embeds import WelcomeEmbed


logger = get_logger()
_ = get_localizator("members.activity")


WELCOME_MESSAGE_DELETE_TIMER = 60 * 3


class OnGuildActivityCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self._bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member) -> None:
        if not API_REQUIRED:
            return

        guild_id = member.guild.id
        user_id = member.id
        member_data = await get_member(guild_id, user_id)

        logger.info(
            "Новый участник [<@%d>] заходит на сервер!\n\n" +
            "**Кол-во участников на сервере: **%d\n**Id пользователя:** %d",
            member.id, member.guild.member_count, user_id,
            extra={
                "user_avatar": member.display_avatar.url,
                "type": "guild",
                "guild_id": member.guild.id
            })
        
        await self._send_welcome_message(member)

        if member_data and not member_data.is_active:
            await member_joined(guild_id, user_id)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member) -> None:
        if not API_REQUIRED:
            return

        guild_id = member.guild.id
        user_id = member.id
        member_data = await get_member(guild_id, user_id)
 
        logger.info(
            "Участник [<@%d>] покидает сервер.\n\n" +
            "**Кол-во участников на сервере: **%d\n**Id пользователя:** %d\n**Присоединился: **<t:%d:F>",
            member.id, member.guild.member_count, user_id, member.joined_at.timestamp(), # type: ignore
            extra={
                "user_avatar": member.display_avatar.url,
                "type": "guild",
                "guild_id": member.guild.id
            })

        if member_data and member_data.is_active:
            await member_left(guild_id, user_id)

    @commands.Cog.listener()
    async def on_member_update(
        self,
        before: disnake.Member,
        after: disnake.Member
    ) -> None:
        await self._log_common_updates(before, after)

    @commands.Cog.listener()
    async def on_user_update(
        self,
        before: disnake.User,
        after: disnake.User
    ) -> None:
        await self._log_common_updates(before, after)

    async def _log_common_updates(
        self,
        before: Union[disnake.Member, disnake.User],
        after: Union[disnake.Member, disnake.User],
    ) -> None:
        self._check_for_log_avatar(before, after)
        await self._check_for_log_username(before, after)

    def _check_for_log_avatar(
        self,
        before: Union[disnake.Member, disnake.User],
        after: Union[disnake.Member, disnake.User],
    ) -> None:
        if before.display_avatar != after.display_avatar:
            logger.warning(
                "Аватар пользователя <@%d> был изменён!", after.id,
                extra={
                    "user_avatar": after.display_avatar.url,
                    "type": "members",
                    "guild_id": before.guild.id if isinstance(before, disnake.Member) else BASE_GUILD_ID
                })

    async def _check_for_log_username(
        self,
        before: Union[disnake.Member, disnake.User],
        after: Union[disnake.Member, disnake.User],
    ) -> None:
        changed_by = None
        if before.display_name != after.display_name:
            if isinstance(before, disnake.Member):
                changed_by = await check_for_mod_actions(
                    guild=before.guild,
                    action=disnake.AuditLogAction.member_update,
                    user_id=before.id
                )
            warning_message = (f"Никнейм пользователя <@{after.id}> был изменён!\n"
                               f"`{before.display_name}` **->** `{after.display_name}`")
            if changed_by:
                warning_message += f"\n\n**Модератор:** {changed_by.mention}"

            logger.warning(
                warning_message,
                extra={
                    "user_avatar": after.display_avatar.url,
                    "type": "members",
                    "guild_id": before.guild.id if isinstance(before, disnake.Member) else BASE_GUILD_ID
                })

    async def _send_welcome_message(self, member: disnake.Member) -> None:
        from src.config import cfg
        channels_cfg = cfg.channels_cfg(member.guild.id)

        if not (general := channels_cfg.general_channel_id):
            logger.warning("general channel is not configured")
            return

        offtop_channel = self._bot.get_channel(general)
        if not isinstance(offtop_channel, disnake.TextChannel):
            logger.warning("general channel [%s] is not text channel", general)
            return

        embed = WelcomeEmbed(
            title=_("activity_listeners_welcome_embed_title"),
            description=_("activity_listeners_welcome_embed_desc")
        )
        await offtop_channel.send(
            member.mention,
            embed=embed,
            delete_after=WELCOME_MESSAGE_DELETE_TIMER
        )
        
