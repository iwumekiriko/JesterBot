import time
import disnake
from disnake.ext import commands, tasks

from src.bot import JesterBot
from ._api_interaction import add_voice_time
from src.logger import get_logger
from src.utils._convertes import user_avatar
from src.utils._tasks import loop

logger = get_logger()


class VoiceActivityListenerCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self.bot = bot
        self._counter: dict[disnake.Member, float] = {}

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

        elif before.channel is not None and after.channel is None:
            logger.debug("Пользователь <@%d> выходит из войс канала [%s]",
                        member.id, before.channel.jump_url,
                        extra={"user_avatar": member.display_avatar.url})
            await add_voice_time(member, int(time.time() - self._counter.pop(member)))

        elif before.channel is not None and after.channel is not None:
            logger.debug("Пользователь <@%d> переходит в войс канал [%s] **->** [%s]",
                        member.id, before.channel.jump_url, after.channel.jump_url,
                        extra={"user_avatar": member.display_avatar.url})
            await add_voice_time(member, int(time.time() - self._counter.pop(member)))
            self.count_user(member)