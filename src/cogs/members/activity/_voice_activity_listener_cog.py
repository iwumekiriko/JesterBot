import time
import disnake
from disnake.ext import commands, tasks

from src.bot import JesterBot
from .._api_interaction import add_voice_time
from src.cogs.economy._api_interaction import update_member_coins
from src.logger import get_logger
from src.utils._experience import is_new_lvl, ExpTypes
from .._utils import send_reward_message, check_for_mod_actions


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
            logger.info("Пользователь <@%d> присоединяется к войс каналу [%s]",
                        member.id, after.channel.jump_url,
                        extra={
                            "user_avatar": member.display_avatar.url,
                            "type": "voice",
                            "guild_id": member.guild.id
                        })
            self.count_user(member)

        elif before.channel is not None and after.channel is None:
            disconnected_by = await check_for_mod_actions(
                guild=member.guild,
                action=disnake.AuditLogAction.member_disconnect,
                user_id=member.id
            )

            info_message = f"Пользователь <@{member.id}> покидает войс канал [{before.channel.jump_url}]"
            if disconnected_by:
                info_message += f"\n\n**Модератор**: {disconnected_by.mention}"

            logger.info(
                info_message,
                extra={
                    "user_avatar": member.display_avatar.url,
                    "type": "voice",
                    "guild_id": member.guild.id
                })

            await self._sync_user(member)

        elif (before.channel is not None and after.channel is not None 
                and before.channel != after.channel):
            moved_by = await check_for_mod_actions(
                guild=member.guild,
                action=disnake.AuditLogAction.member_move,
                user_id=member.id
            )

            info_message = (f"Пользователь <@{member.id}> переходит в войс канал"
                            f"[{before.channel.jump_url}] **->** [{after.channel.jump_url}]")
            if moved_by:
                info_message += f"\n\n**Модератор**: {moved_by.mention}"

            logger.info(
                info_message,
                extra={
                    "user_avatar": member.display_avatar.url,
                    "type": "voice",
                    "guild_id": before.channel.guild.id
                })

            await self.sync_user_in_vc(member)


    async def _add_time(self, member: disnake.Member, seconds: int) -> None:
        if member.bot:
            return

        member_data = await add_voice_time(member, seconds)
        is_lvled, coins = is_new_lvl(member_data, ExpTypes.VOICE)
        if is_lvled:
            await update_member_coins(member_data.guild_id, member_data.user_id, coins)
            await send_reward_message(member_data, coins)
