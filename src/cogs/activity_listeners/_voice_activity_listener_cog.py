import time
import disnake
from disnake.ext import commands

from src.bot import JesterBot
from ._api_interaction import add_voice_time, add_coins
from src.logger import get_logger
from src.utils._tasks import loop1
from src.utils._experience import is_new_lvl
from ._utils import send_reward_message


logger = get_logger()


class VoiceActivityListenerCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self.bot = bot
        self._counter: dict[disnake.Member, float] = {}

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.sync.start(self) # type: ignore

    @loop1(seconds=60)
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

    def count_user(self, member: disnake.Member):
        self._counter[member] = self._counter.get(member, time.time())

    async def _sync_user(self, member: disnake.Member):
        await self._add_time(member, int(time.time() - self._counter.pop(member)))

    async def sync_user_in_vc(self, member: disnake.Member):
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
        member_data = await add_voice_time(member, seconds)
        is_lvled, coins = is_new_lvl(member_data, "voice")
        if is_lvled:
            from src.config import cfg
            offtop_id = cfg.channels_cfg(member.guild.id).offtop_channel_id or 0
            await add_coins(member_data, coins)
            await send_reward_message(member_data, offtop_id, coins)
