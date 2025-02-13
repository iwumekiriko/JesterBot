import time
import disnake
from disnake.ext import commands, tasks

from src.bot import JesterBot
from .._api_interaction import add_voice_time
from src.cogs.economy._api_interaction import coins_
from src.logger import get_logger
from src.utils._experience import is_new_lvl, ExpTypes
from .._utils import send_reward_message


logger = get_logger()


class VoiceActivityListenerCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self._bot = bot
        self._counter: dict[disnake.Member, float] = {}
        self.sync.start()

    def cog_unload(self) -> None:
        self.sync.cancel()

    @tasks.loop(minutes=1)
    async def sync(self) -> None:
        if not self._counter:
            return

        await self._sync()

    async def _sync(self) -> None:
        try:
            for member, join_time in self._counter.items():
                current_time = time.time()
                voice_seconds = int(current_time - join_time)
                try:
                    await self._add_time(member, voice_seconds)
                    self._counter[member] = current_time
                except:
                    self.count_user(member)
        except RuntimeError:
            pass

    def count_user(self, member: disnake.Member) -> None:
        self._counter[member] = self._counter.get(member, time.time())

    async def _sync_user(self, member: disnake.Member) -> None:
        await self._add_time(member, int(time.time() - self._counter.pop(member)))

    async def sync_user_in_vc(self, member: disnake.Member) -> None:
        await self._sync_user(member)
        self.count_user(member)

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
            logger.info("Пользователь <@%d> заходит в войс канал [%s]",
                        member.id, after.channel.jump_url,
                        extra={"user_avatar": member.display_avatar.url, "type": "voice"})
            self.count_user(member)

        elif before.channel is not None and after.channel is None:
            logger.info("Пользователь <@%d> выходит из войс канала [%s]",
                        member.id, before.channel.jump_url,
                        extra={"user_avatar": member.display_avatar.url, "type": "voice"})
            await self._sync_user(member)

        elif (before.channel is not None and after.channel is not None 
                and before.channel != after.channel):
            logger.info("Пользователь <@%d> переходит в войс канал [%s] **->** [%s]",
                        member.id, before.channel.jump_url, after.channel.jump_url,
                        extra={"user_avatar": member.display_avatar.url, "type": "voice"})
            await self.sync_user_in_vc(member)


    async def _add_time(self, member: disnake.Member, seconds: int) -> None:
        if member.bot:
            return

        member_data = await add_voice_time(member, seconds)
        is_lvled, coins = is_new_lvl(member_data, ExpTypes.VOICE)
        if is_lvled:
            await coins_(member_data.guild_id, member_data.user_id, coins)
            await send_reward_message(member_data, coins)
