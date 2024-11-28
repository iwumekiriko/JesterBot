import asyncio
import disnake
from disnake.ext import commands

from src.logger import get_logger
from src.bot import JesterBot
from src._config import CUSTOM_VOICE_CATEGORY_ID, CUSTOM_VOICE_CREATION_CHANNEL
from src.utils._convertes import user_avatar


logger = get_logger()


CUSTOM_VOICE_DELETE_TIME = 120


class CustomVoiceCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self.bot = bot
        self._delete_timers = {}

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: disnake.Member,
        before: disnake.VoiceState,
        after: disnake.VoiceState
    ) -> None:
        if member.bot:
            return

        if after.channel is not None:
            await self._check_for_custom_voice(member, after.channel) # type: ignore
            
        await self._check_for_delete(before.channel, after.channel) # type: ignore


    
    async def _check_for_custom_voice(
        self,
        member: disnake.Member,
        channel: disnake.VoiceChannel
    ) -> None:
        if CUSTOM_VOICE_CREATION_CHANNEL != channel.id:
            return
        
        voice_category = channel.category
        if not voice_category:
            return
        
        custom_channel = await voice_category.create_voice_channel(
            name = f"Канал пользователя {member.name}"
        )
        try:
            await member.move_to(custom_channel)
        except:
            logger.warning("Не удалось перенести пользователя <@%d> в кастомный войс канал.", member.id,
                         extra={"user_avatar": user_avatar(jester=True)})

    async def _check_for_delete(
        self,
        before_channel: disnake.VoiceChannel | None,
        after_channel: disnake.VoiceChannel | None,
    ) -> None:        
        if before_channel is None:
            return

        if before_channel.category and not before_channel.category.id == CUSTOM_VOICE_CATEGORY_ID:
            return
        
        if before_channel.id == CUSTOM_VOICE_CREATION_CHANNEL:
            return
        
        if before_channel.members:
            return
        
        if after_channel is not None and after_channel.id in self._delete_timers:
            self._delete_timers[after_channel.id].cancel()
            del self._delete_timers[after_channel.id]
            logger.debug("Голосовой канал [%s] больше не в состоянии удаления.", after_channel.jump_url,
                            extra={"user_avatar": user_avatar(jester=True)})
            return

        async def delete_channel(channel: disnake.VoiceChannel):
            await asyncio.sleep(CUSTOM_VOICE_DELETE_TIME)
            try:
                await channel.delete()
            except:
                logger.warning("Попытка удалить кастомный войс [%s] (id: %d) канал прошла неудачно.",
                                channel.jump_url, channel.id,
                               extra={"user_avatar": user_avatar(jester=True)})

        task = asyncio.create_task(delete_channel(before_channel))
        logger.debug("Голосовой канал [%s] удалится через %d секунд",
                     before_channel.jump_url, CUSTOM_VOICE_DELETE_TIME,
                     extra={"user_avatar": user_avatar(jester=True)})
        self._delete_timers[before_channel.id] = task
        
