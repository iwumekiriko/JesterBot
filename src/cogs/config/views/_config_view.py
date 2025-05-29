import disnake
from typing import Optional, Callable

from src.localization import get_localizator
from src.logger import get_logger
from src.utils.ui._views import BaseView
from .._modal_forms import *
from src.config import cfg
from src.models.config.base_config import BaseConfig
from src.utils.ui._embeds import BaseEmbed


logger = get_logger()
_ = get_localizator("config.common")


class ConfigView(BaseView):
    def __init__(
        self,
        guild_id: int
    ) -> None:
        super().__init__(timeout=300)
        self.guild_id = guild_id
        self.current_cfg: tuple[BaseConfig, int] = (cfg.exp_cfg(guild_id), 0)

        self.config_map: dict[tuple[str, Optional[str]], str] = {
            (_("experience_cfg_0"), "🧪"): "exp_cfg",
            (_("roles_cfg_0"), "🥐"): "roles_cfg",
            (_("channels_cfg_0"), "🍵"): "channels_cfg",
            (_("shop_cfg_0"), "🛒"): "shop_cfg",
            (_("tickets_cfg_0"), "🎟️"): "tickets_cfg",
            (_("voice_cfg_0"), "🔊"): "voice_cfg",
            (_("logs_cfg_0"), "🕸️"): "logs_cfg",
            (_("logs_cfg_1"), "🕸️"): "logs_cfg",
            (_("lootboxes_cfg_0"), "🎁"): "lootboxes_cfg",
            (_("economy_cfg_0"), "🪙"): "economy_cfg",
            (_("quests_cfg_0"), "❗"): "quests_cfg",
        }

        self.config_modals: dict[str, Callable] = {
            "Experience": experience_cfg_modal_form,
            "Roles": roles_cfg_modal_form,
            "Channels": channels_cfg_modal_form,
            "Shop": shop_cfg_modal_form,
            "Tickets": tickets_cfg_modal_form,
            "Voice": voice_cfg_modal_form,
            "Logs": logs_cfg_modal_form,
            "Lootboxes": lootboxes_cfg_modal_form,
            "Economy": economy_cfg_modal_form,
            "Quests": quests_cfg_modal_form,
        }

        self.add_item(ConfigSelect(self.config_map))
        self.add_item(ChangeCfgButton())

    def create_embed(self) -> disnake.Embed:
        cfg = self.current_cfg[0]
        page = self.current_cfg[1]
        desc = ""

        for field, value in (
            (fields := list(vars(cfg).items()))
            [(start:=page*5+2):min(start+5, len(fields))]
        ):
            if isinstance(value, str) and len(value) > 40:
                value = f"{value[:35]}...{value[-5:]}"
            desc += f"**{_(field + '_field')}: **\n```{value}```\n"

        return BaseEmbed(
            title=_(f"{cfg.short_name.lower()}_config_embed_title"),
            description=desc
        )
    
    async def _response(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(
            embed=self.create_embed(),
            view=self,
        )
    

class ConfigSelect(disnake.ui.Select):
    view: ConfigView

    def __init__(self, config_map: dict) -> None:
        options = [disnake.SelectOption(
            label = name, emoji = emoji
        ) for name, emoji in config_map]
        super().__init__(options=options)

    async def callback(
        self,
        interaction: disnake.MessageInteraction
    ) -> None:
        view = self.view
        name = self.values[0]
        self.view.current_cfg = (getattr(cfg, next((
            value for key, value in view.config_map.items()
                if key[0] == name)))(interaction.guild_id), int(name[-1]) - 1)
        await interaction.response.edit_message(
            embed = view.create_embed(),
            view = view
        )


class ChangeCfgButton(disnake.ui.Button):
    view: ConfigView

    def __init__(self) -> None:
        super().__init__(
            label=_("change_cfg_button"),
            style=disnake.ButtonStyle.grey
        )

    async def callback(
        self,
        interaction: disnake.MessageCommandInteraction
    ) -> None:
        view = self.view
        cfg = view.current_cfg[0]
        params = {f"base_{k}": v for k, v in vars(cfg).items() if k not in ['guild_id', 'guild']}
        inter: disnake.ModalInteraction | None = (
            await view.config_modals[cfg.short_name]
            (interaction, **params, page=view.current_cfg[1]))
        if not inter:
            return
        
        await inter.response.edit_message(
            embed=view.create_embed(),
            view=view
        )