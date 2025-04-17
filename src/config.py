from dotenv import load_dotenv

load_dotenv()

from src.models.config import *
from src.models.config.base_config import BaseConfig
from ._api_interaction import get_cfg
from src.settings import BASE_GUILD_ID, API_REQUIRED
from _manual_config import *


class Config:
    def __init__(self) -> None:
        self.__cfg = {}
        self.base_guild_id = BASE_GUILD_ID

    @property
    def config(self) -> dict:
        return self.__cfg

    def exp_cfg(self, guild_id: int) -> ExperienceConfig:
        return self.__cfg[guild_id]["Experience"]

    def roles_cfg(self, guild_id: int) -> RolesConfig:
        return self.__cfg[guild_id]["Roles"]

    def channels_cfg(self, guild_id: int) -> ChannelsConfig:
        return self.__cfg[guild_id]["Channels"]

    def shop_cfg(self, guild_id: int) -> ShopConfig:
        return self.__cfg[guild_id]["Shop"]

    def tickets_cfg(self, guild_id: int) -> TicketsConfig:
        return self.__cfg[guild_id]["Tickets"]

    def voice_cfg(self, guild_id: int) -> VoiceConfig:
        return self.__cfg[guild_id]["Voice"]

    def logs_cfg(self, guild_id: int) -> LogsConfig:
        return self.__cfg[guild_id]["Logs"]
    
    def lootboxes_cfg(self, guild_id: int) -> LootboxesConfig:
        return self.__cfg[guild_id]["Lootboxes"]
    
    def economy_cfg(self, guild_id: int) -> EconomyConfig:
        return self.__cfg[guild_id]["Economy"]

    async def _load_cfg(self) -> None:
        from src.bot import bot
        cfgs: list[type[BaseConfig]] = [ExperienceConfig,
                                        RolesConfig,
                                        ChannelsConfig,
                                        ShopConfig,
                                        TicketsConfig,
                                        VoiceConfig,
                                        LogsConfig,
                                        LootboxesConfig,
                                        EconomyConfig]

        local_cfg = {}
        for c in cfgs:
            if API_REQUIRED:
                for guild in bot.guilds:
                    config = await get_cfg(guild.id, c)
                    if guild.id not in self.__cfg:
                        self.__cfg[guild.id] = {}
                    self.__cfg[guild.id][c(0).short_name] = config

            else:
                config = self._get_manually(c)
                local_cfg[c(0).short_name] = config

        if not API_REQUIRED:
            self.__cfg[self.base_guild_id] = local_cfg

    def _get_manually(self, c: type[BaseConfig]) -> BaseConfig:
        config = c(self.base_guild_id)

        match config:
            case ExperienceConfig():
                config.exp_for_message = EXP_FOR_MESSAGE
                config.exp_for_voice_minute = EXP_FOR_VOICE_MINUTE

            case RolesConfig():
                config.support_role_id = SUPPORT_ROLE_ID
                config.moderator_role_id = MODERATOR_ROLE_ID
                config.developer_role_id = DEVELOPER_ROLE_ID

            case ChannelsConfig():
                config.general_channel_id = GENERAL_CHANNEL_ID
                config.offtop_channel_id = OFFTOP_CHANNEL_ID

            case ShopConfig():
                config.shop_channel_id = SHOP_CHANNEL_ID
                config.shop_message_id = SHOP_MESSAGE_ID

            case TicketsConfig():
                config.ticket_channel_id = TICKET_CHANNEL_ID
                config.ticket_message_id = TICKET_MESSAGE_ID
                config.ticket_report_channel_id = TICKET_REPORT_CHANNEL_ID

            case VoiceConfig():
                config.custom_voice_creation_channel_id = CUSTOM_VOICE_CREATION_CHANNEL_ID
                config.custom_voice_category_id = CUSTOM_VOICE_CATEGORY_ID
                config.custom_voice_deletion_time = CUSTOM_VOICE_DELETION_TIME

            case LogsConfig():
                config.command_interactions_webhook_url = COMMAND_INTERACTIONS_WEBHOOK_URL
                config.messages_webhook_url = MESSAGES_WEBHOOK_URL
                config.tickets_webhook_url = TICKETS_WEBHOOK_URL
                config.guild_webhook_url = GUILD_WEBHOOK_URL
                config.members_webhook_url = MEMBERS_WEBHOOK_URL
                config.else_webhook_url = ELSE_WEBHOOK_URL

            case LootboxesConfig():
                config.roles_lootbox_key_price = ROLES_LOOTBOX_KEYS_PRICE
                config.backgrounds_lootbox_key_price = BACKGROUNDS_LOOTBOX_KEYS_PRICE

            case EconomyConfig():
                config.daily_bonus = DAILY_BONUS
                config.default_currency_icon = DEFAULT_CURRENCY_ICON
                config.donate_currency_icon = DONATE_CURRENCY_ICON

        return config

    def _set_cfg(self, cfg: BaseConfig) -> None:
        local_cfg = self.__cfg[cfg.guild_id][cfg.short_name]
        for attr_name in vars(cfg):
            attr_value = getattr(cfg, attr_name)
            if attr_value is not None:
                setattr(local_cfg, attr_name, attr_value)

    async def load(self) -> None:
        await self._load_cfg()

    def set_(self, cfg: BaseConfig) -> None:
        self._set_cfg(cfg)


cfg = Config()
