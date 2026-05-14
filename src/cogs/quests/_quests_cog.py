import datetime
from typing import Any, Dict, Optional, Tuple, List
import asyncio

import disnake
from disnake.ext import commands, tasks

from src.bot import JesterBot
from src.localization import get_localizator
from src.logger import get_logger

from ._api_interaction import (
    get_user_quests,
    handle_quest_template,
    set_quests_message,
    update_quests
)
from .views import QuestsPaginator, QuestsBoardView
from src.utils.ui import SuccessEmbed, ViewSwitcher
from src.utils.enums import Actions
from src.utils._converters import user_avatar
from src.utils._time import seconds_until_next_day
from src.models.quests import QuestRewardTypes, QuestTaskTypes, QuestTypes, Quest
from src.models.config import QuestsConfig
from src.customisation import QUESTS_KEEPER_NAME, QUESTS_KEEPER_AVATAR
from src.utils._permissions import for_admins


_ = get_localizator("quests.common")
logger = get_logger()


CONFIG_LOAD_TIME = 3


class QuestsCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self._bot = bot
        self.quests_update.start()

    def cog_unload(self) -> None:
        self.quests_update.cancel()

    @tasks.loop(hours=24)
    async def quests_update(self) -> None:
        await update_quests()
        await self.update_quests_board()

    @quests_update.before_loop
    async def before_quests_update(self) -> None:
        await self._bot.wait_until_ready()
        await self.wait_for_midnight()

    async def wait_for_midnight(self) -> None:
        sleep_time = seconds_until_next_day()
        logger.info("quests update will sleep for %d seconds", sleep_time)
        await asyncio.sleep(sleep_time)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await asyncio.sleep(CONFIG_LOAD_TIME)
        from src.config import cfg

        for guild in self._bot.guilds:
            quests_cfg = cfg.quests_cfg(guild.id)
            await self._process_guild_quests(guild, quests_cfg, init_mode=True)

        logger.info("Quest channels for guilds %s are ready.",
                    [guild.id for guild in self._bot.guilds])

    async def update_quests_board(self) -> None:
        from src.config import cfg

        for guild in self._bot.guilds:
            quests_cfg = cfg.quests_cfg(guild.id)
            await self._process_guild_quests(guild, quests_cfg, init_mode=False)

    async def _process_guild_quests(self, guild: disnake.Guild, quests_cfg: QuestsConfig, init_mode: bool) -> None:
        quests_channel = await self._get_quests_channel(guild, quests_cfg)

        if not quests_channel:
            return

        message = await self._get_quests_message(quests_channel, quests_cfg)

        if init_mode:
            if not message:
                await self._create_board_message(quests_channel)
                logger.debug("Создано новое сообщение доски объявлений",
                          extra=self._log_extra_params(guild.id))

        else:
            if message:
                await message.delete()
            await self._create_board_message(quests_channel)
            logger.info("Доска объявлений обновлена",
                      extra=self._log_extra_params(guild.id))

    async def _get_quests_channel(
        self,
        guild: disnake.Guild,
        quests_cfg: QuestsConfig
    ) -> Optional[disnake.TextChannel]:
        if not (qci := quests_cfg.quests_channel_id):
            return None

        channel = guild.get_channel(qci)
        if not isinstance(channel, disnake.TextChannel):
            logger.debug("Канал для квестов недоступен!", extra=self._log_extra_params(guild.id))
            return None

        return channel

    async def _get_quests_message(
        self,
        channel: disnake.TextChannel,
        quests_cfg: QuestsConfig
    ) -> Optional[disnake.Message]:
        if not (qmi := quests_cfg.quests_message_id):
            return None

        try:
            return await channel.fetch_message(qmi)
        except (disnake.NotFound, disnake.Forbidden, disnake.HTTPException):
            return None

    async def _create_board_message(self, channel: disnake.TextChannel) -> None:
        view = QuestsBoardView()
        await view.set_board_img(channel.guild.id)

        webhook = next((wh for wh in await channel.webhooks() if wh.name == QUESTS_KEEPER_NAME), None)
        if not webhook:
            webhook = await channel.create_webhook(name=QUESTS_KEEPER_NAME)
        message = await webhook.send(
            avatar_url=QUESTS_KEEPER_AVATAR,
            username=QUESTS_KEEPER_NAME,
            embed=view.create_embed(),
            view=view, wait=True
        )
        await set_quests_message(channel.guild.id, message.id)

    def _log_extra_params(self, guild_id: int) -> Dict:
        return {
            "user_avatar": user_avatar(jester=True),
            "type": "else",
            "guild_id": guild_id
        }

    @commands.slash_command(description=_("quests-desc"))
    async def quests(
        self,
        interaction: disnake.GuildCommandInteraction
    ) -> None:
        user_quests = await get_user_quests(
            interaction.guild.id, interaction.user.id
        )
        view = QuestsPaginator(items=user_quests, on_board=False)
        await view.start(interaction, kwargs={"quests": user_quests})

    @commands.slash_command(**for_admins, description=_("quest_template_desc"))
    async def _qt(
        self,
        interaction: disnake.GuildCommandInteraction,
        action = commands.Param(
            choices={ action.get_translated_name(): action for action in Actions },
            description=_("quest_template-action_param")),
        time_type = commands.Param(
            choices={ type.get_translated_name(): type for type in QuestTypes },
            description=_("quest_template-time_type_param")),
        task_type = commands.Param(
            choices={ type.get_translated_name(): type for type in QuestTaskTypes },
            description=_("quest_template-task_type_param")),
        required: int = commands.Param(description=_("quest_template-required_param")),
        reward_type = commands.Param(
            choices={ type.get_translated_name(): type for type in QuestRewardTypes },
            description=_("quest_template-reward_type_param")),
        reward_amount: int = commands.Param(description=_("quest_template-reward_amount_param")),
        weight: float = commands.Param(description=_("quest_template-weight_param")),
        channel: disnake.TextChannel | disnake.VoiceChannel | disnake.StageChannel = commands.Param(
            converter=None, description=_("quest_template-channel_param"))
    ) -> None:
        if required == 0 or reward_amount == 0:
            raise commands.BadArgument(_("quests-required_or_reward_equals_zero_error"))
        
        await interaction.response.defer(ephemeral=True)
        await handle_quest_template(
            action,
            interaction.guild.id,
            time_type,
            task_type,
            abs(required),
            reward_type,
            abs(reward_amount),
            abs(weight),
            channel.id if channel else None
        )
        response = {
            Actions.ADD: _("quests-template-add_success",
                                        type=QuestTypes(time_type).get_translated_name(),
                                        task_type=QuestTaskTypes(task_type).get_translated_name(),
                                        required=required),
            Actions.REMOVE: _("quests-template-remove_success",
                                        type=QuestTypes(time_type).get_translated_name(),
                                        task_type=QuestTaskTypes(task_type).get_translated_name(),
                                        required=required)
        }
        await interaction.followup.send(embed=SuccessEmbed(success_msg=response[action]))


class QuestsHistoryViewSwitcher(ViewSwitcher):
    async def _response(
        self,
        view: Any,
        interaction: disnake.MessageInteraction
    ) -> None:
        await interaction.response.edit_message(
            embed=view.create_embed(),
            view=view
        )
