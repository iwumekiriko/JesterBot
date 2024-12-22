import asyncio
import disnake
from disnake.ext import commands

from src.logger import get_logger
from src.bot import JesterBot
from src.utils._convertes import user_avatar


logger = get_logger()


CUSTOM_VOICE_DELETE_TIME = 30


class CustomVoiceCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self.bot = bot
        self._delete_timers: dict[int, asyncio.Task] = {}

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: disnake.Member,
        before: disnake.VoiceState,
        after: disnake.VoiceState
    ) -> None:
        if member.bot:
            return

        if isinstance(after.channel, disnake.VoiceChannel):
            await self._check_for_custom_voice(member, after.channel)
            await self._check_for_timer_stop(after.channel)

        if isinstance(before.channel, disnake.VoiceChannel):
            await self._check_for_delete(before.channel)


    async def _check_for_custom_voice(
        self,
        member: disnake.Member,
        channel: disnake.VoiceChannel
    ) -> None:
        from src.config import cfg

        guild_id = channel.guild.id
        voice_cfg = cfg.voice_cfg(guild_id)

        CUSTOM_VOICE_CREATION_CHANNEL_ID = voice_cfg.custom_voice_creation_channel_id

        if channel.id != CUSTOM_VOICE_CREATION_CHANNEL_ID:
            return

        voice_category = channel.category
        if not voice_category:
            return

        custom_channel = await voice_category.create_voice_channel(
            name = f"Канал {member.name}")
        await custom_channel.set_permissions(
            member, manage_channels=True, view_channel=True, connect=True)
        try:
            await member.move_to(custom_channel)
        except:
            logger.warning("Не удалось перенести пользователя <@%d> в кастомный войс канал.",
                            member.id, extra={"user_avatar": user_avatar(jester=True), "type": "voice"})

    async def _check_for_delete(
        self,
        before_channel: disnake.VoiceChannel
    ) -> None:
        from src.config import cfg

        guild_id = before_channel.guild.id
        voice_cfg = cfg.voice_cfg(guild_id)

        CUSTOM_VOICE_CREATION_CHANNEL_ID = voice_cfg.custom_voice_creation_channel_id
        CUSTOM_VOICE_CATEGORY_ID = voice_cfg.custom_voice_category_id
        CUSTOM_VOICE_DELETE_TIME = voice_cfg.custom_voice_deletion_time or 30


        if before_channel.category and not before_channel.category.id == CUSTOM_VOICE_CATEGORY_ID:
            return

        if before_channel.id == CUSTOM_VOICE_CREATION_CHANNEL_ID:
            return

        if before_channel.members:
            return

        async def delete_channel(channel: disnake.VoiceChannel):
            await asyncio.sleep(CUSTOM_VOICE_DELETE_TIME)
            try:
                await channel.delete()
            except:
                logger.debug("Попытка удалить кастомный войс [%s | %s] канал прошла неудачно.",
                               channel.jump_url, channel.name,
                               extra={"user_avatar": user_avatar(jester=True), "type": "else"})

        task = asyncio.create_task(delete_channel(before_channel))
        logger.debug("Голосовой канал [%s | %s] удалится через %d секунд",
                     before_channel.jump_url, before_channel.name, CUSTOM_VOICE_DELETE_TIME,
                     extra={"user_avatar": user_avatar(jester=True)})
        self._delete_timers[before_channel.id] = task

    async def _check_for_timer_stop(
        self,
        after_channel: disnake.VoiceChannel
    ) -> None:
        if after_channel.id not in self._delete_timers:
            return

        self._delete_timers[after_channel.id].cancel()
        del self._delete_timers[after_channel.id]
        logger.debug("Голосовой канал [%s | %s] больше не подлежит тотальному уничтожению!!!!",
                        after_channel.jump_url, after_channel.name,
                        extra={"user_avatar": user_avatar(jester=True), "type": "else"})