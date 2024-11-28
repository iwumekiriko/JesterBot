import asyncio
import time
import disnake
from disnake.ext import commands

from src.bot import JesterBot
from ._api_interaction import add_voice_time
from src.logger import get_logger
from src.utils._tasks import loop
from src._config import CUSTOM_VOICE_CREATION_CHANNEL, CUSTOM_VOICE_CATEGORY_ID
from src.utils._convertes import user_avatar


logger = get_logger()


CUSTOM_VOICE_DELETE_TIME = 10


class VoiceActivityListenerCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self.bot = bot
        self._counter: dict[disnake.Member, float] = {}
        self._delete_timers = {}

    @loop(minutes=1)
    async def sync(self) -> None:
        if not self._counter:
            return

        await self._sync()

    async def _sync(self) -> None:
        for member, join_time in self._counter.items():
            current_time = time.time()
            voice_seconds = int(current_time - join_time)
            await add_voice_time(member, voice_seconds)
            self._counter[member] = current_time

    def count_user(self, member: disnake.Member):
        self._counter[member] = self._counter.get(member, time.time())

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: disnake.Member,
        before: disnake.VoiceState,
        after: disnake.VoiceState
    ) -> None:
        if member.bot:
            return
        
        if before.channel is None and after.channel is not None:
            logger.debug("Пользователь <@%d> заходит в войс канал [%s]",
                        member.id, after.channel.jump_url,
                        extra={"user_avatar": member.display_avatar.url})
            self.count_user(member)
            await self._check_for_custom_voice(member, after.channel) # type: ignore

        elif before.channel is not None and after.channel is None:
            logger.debug("Пользователь <@%d> выходит из войс канала [%s]",
                        member.id, before.channel.jump_url,
                        extra={"user_avatar": member.display_avatar.url})
            await add_voice_time(member, int(time.time() - self._counter.pop(member)))

        elif (before.channel is not None and after.channel is not None 
                and before.channel != after.channel):
            logger.debug("Пользователь <@%d> переходит в войс канал [%s] **->** [%s]",
                        member.id, before.channel.jump_url, after.channel.jump_url,
                        extra={"user_avatar": member.display_avatar.url})
            await add_voice_time(member, int(time.time() - self._counter.pop(member)))
            self.count_user(member)
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
            logger.error("Не удалось перенести пользователя <@%d> в кастомный войс канал.", member.id,
                         extra={"user_avatar": user_avatar(jester=True)})

    async def _check_for_delete(
        self,
        before_channel: disnake.VoiceChannel | None,
        after_channel: disnake.VoiceChannel | None,
    ) -> None:
        if before_channel is None:
            if after_channel and after_channel.id in self._delete_timers:
                self._delete_timers[after_channel.id].cancel()
                del self._delete_timers[after_channel.id]
                logger.debug("Голосовой канал [%s] больше не в состоянии удаления.", after_channel.jump_url,
                             extra={"user_avatar": user_avatar(jester=True)})
            return
        
        if before_channel is not None and after_channel is not None:
            if after_channel.id in self._delete_timers:
                self._delete_timers[after_channel.id].cancel()
                del self._delete_timers[after_channel.id]
                logger.debug("Голосовой канал [%s] больше не в состоянии удаления.", after_channel.jump_url,
                             extra={"user_avatar": user_avatar(jester=True)})
            return

        if before_channel.category and not before_channel.category.id == CUSTOM_VOICE_CATEGORY_ID:
            return
        
        if before_channel.id == CUSTOM_VOICE_CREATION_CHANNEL:
            return
        
        if before_channel.members:
            return
        
        async def delete_channel(channel: disnake.VoiceChannel):
            await asyncio.sleep(CUSTOM_VOICE_DELETE_TIME)
            try:
                await channel.delete()
            except:
                logger.warning("Попытка удалить кастомный войс [%s] (id: %d) канал прошла неуспешно.",
                                channel.jump_url, channel.id,
                               extra={"user_avatar": user_avatar(jester=True)})

        task = asyncio.create_task(delete_channel(before_channel))
        logger.debug("Голосовой канал [%s] удалится через %d секунд",
                     before_channel.jump_url, CUSTOM_VOICE_DELETE_TIME,
                     extra={"user_avatar": user_avatar(jester=True)})
        self._delete_timers[before_channel.id] = task
        

        

