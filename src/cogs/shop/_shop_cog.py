import asyncio
from typing import Dict, List
import aiohttp

import disnake
from disnake.ext import commands, tasks

from .views import ShopCreationView
from src.utils._converters import user_avatar, dangerous_role_excluding
from src.utils._permissions import for_admins
from src.utils._extra import remove_role_with_id
from src.utils.enums import Actions
from src.utils.ui import SuccessEmbed
from src.cogs.lootboxes._lootbox_map import LootboxMap
from src.customisation import SHOP_KEEPER_NAME, SHOP_KEEPER_AVATAR
from ._api_interaction import (
    set_shop_message,
    handle_shop_role,
    handle_shop_key,
    reset_shop_roles_tries
)

from src.bot import JesterBot
from src.logger import get_logger
from src.localization import get_localizator


logger = get_logger()
_ = get_localizator("shop.common")
CONFIG_LOAD_TIME = 3


def _active_lootboxes_autocomplete(
    inter: disnake.ApplicationCommandInteraction, arg
) -> Dict[str, str]:
    actives = LootboxMap.actives(inter.guild.id) # type: ignore
    return {lb.translated(): lb.value for lb in actives}


class ShopCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self._bot = bot
        self.shop_roles_tries_reset.start()

    def cog_unload(self) -> None:
        self.shop_roles_tries_reset.cancel()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await asyncio.sleep(CONFIG_LOAD_TIME)

        from src.config import cfg

        for guild in self._bot.guilds:
            shop_cfg = cfg.shop_cfg(guild.id)
            shop_channel_id = shop_cfg.shop_channel_id
            shop_message_id = shop_cfg.shop_message_id

            if not shop_channel_id:
                continue

            shop_channel = self._bot.get_channel(shop_channel_id)
            if not isinstance(shop_channel, disnake.TextChannel):
                logger.debug("Канал для магазиника недоступен!",
                            extra={
                                "user_avatar": user_avatar(jester=True),
                                "type": "else",
                                "guild_id": guild.id
                            })
                continue

            try:
                await shop_channel.fetch_message(shop_message_id) # type: ignore
            except:
                view = ShopCreationView()
                webhook = next((wh for wh in await shop_channel.webhooks() if wh.name == SHOP_KEEPER_NAME), None)
                if not webhook:
                    webhook = await shop_channel.create_webhook(name=SHOP_KEEPER_NAME)
                message = await webhook.send(
                    avatar_url=SHOP_KEEPER_AVATAR,
                    username=SHOP_KEEPER_NAME,
                    embed=view.create_embed(),
                    view=view, wait=True
                )
                logger.debug("Сообщение магазиника не было найдено. Создано новое.",
                            extra={
                                "user_avatar": user_avatar(jester=True),
                                "type": "else",
                                "guild_id": guild.id
                            })
                await set_shop_message(guild.id, message.id)
        logger.info("Shop channels for guilds %s are ready.",
                     [guild.id for guild in self._bot.guilds])

    @commands.slash_command(**for_admins, description=_("shop-role_desc"))
    async def _sr(
        self,
        interaction: disnake.GuildCommandInteraction,
        action = commands.Param(
            choices = { action.get_translated_name(): action for action in Actions },
            description=_("shop-role-action_param")),
        guild_role: disnake.Role = commands.Param(
            converter=dangerous_role_excluding, description=_("shop-role-role_param")),
        price: int = commands.Param(description=_("shop-role-price_param"), default=20000),
        exclusive: bool = commands.Param(description=_("shop-role-exclusive_param"), default=False)
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild
        response = {
            Actions.ADD: _("shop-role-add_success", role_id=guild_role.id),
            Actions.REMOVE: _("shop-role-remove_success", role_id=guild_role.id)
        }
        await handle_shop_role(guild.id, action, guild_role.id, price, exclusive)
        await interaction.followup.send(
            embed=SuccessEmbed(success_msg=response[action])
        )

    @commands.slash_command(**for_admins, description=_("shop-key_desc"))
    async def _sk(
        self,
        interaction: disnake.GuildCommandInteraction,
        action = commands.Param(
            choices = { action.get_translated_name(): action for action in Actions },
            description=_("shop-key-action_param")),
        lootbox_type = commands.Param(
            autocomplete=_active_lootboxes_autocomplete,
            description=_("shop-key-type_param")),
        exclusive: bool = commands.Param(description=_("shop-key-exclusive_param"), default=False)
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild
        l_type = LootboxMap.to_type(lootbox_type)
        response = {
            Actions.ADD: _("shop-key-add_success", lootbox_type=l_type.translated),
            Actions.REMOVE: _("shop-key-remove_success", lootbox_type=l_type.translated)
        }
        await handle_shop_key(guild.id, action, l_type, exclusive)
        await interaction.followup.send(
            embed=SuccessEmbed(success_msg=response[action])
        )

    @tasks.loop(minutes=1)
    async def shop_roles_tries_reset(self) -> None:
        for guild in self._bot.guilds:
            expired_tries = await reset_shop_roles_tries(guild.id)
            if expired_tries:
                user_roles = await self._process_expired_tries(guild, expired_tries)

                if user_roles:
                    log_entries = []
                    for uid, roles in user_roles.items():
                        roles_list = ", ".join(roles)
                        log_entries.append(f"<@{uid}>: ({roles_list})")

                    logger.debug(
                        "У пользователей окончился пробный период ролей:\n %s",
                        "\n ".join(log_entries),
                        extra={
                            "user_avatar": user_avatar(jester=True),
                            "type": "else",
                            "guild_id": guild.id
                        }
                    )

    async def _process_expired_tries(
        self,
        guild: disnake.Guild,
        expired_tries: List[Dict[str, int]]
    ) -> Dict:
        user_roles = {}
    
        for try_record in expired_tries:
            user_id = try_record.get("userId", 0)
            guild_role_id = try_record.get("guildRoleId", 0)
            user = guild.get_member(user_id)
            if not user:
                continue

            removed = await remove_role_with_id(guild, user, guild_role_id)
            if not removed:
                logger.error("Не удалось удалить роль <@&%s> у пользователя <@%s> после примерки",
                              guild_role_id, user_id,
                              extra={
                                  "user_avatar": user_avatar(jester=True),
                                  "type": "else",
                                  "guild_id": guild.id
                              })

            if user_id not in user_roles:
                user_roles[user_id] = []
            user_roles[user_id].append(str(guild_role_id))
        
        return user_roles