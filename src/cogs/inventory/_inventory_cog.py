import disnake
from disnake.ext import commands, tasks

from src.bot import JesterBot
from src.logger import get_logger
from src.localization import get_localizator
from ._api_interaction import get_inventory, reset_boosters
from .views import InventoryCategoriesView
from src.utils._converters import user_avatar


logger = get_logger()
_ = get_localizator("inventory")


class InventoryCog(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot = bot
        self.boosters_reseter.start()

    def cog_unload(self) -> None:
        self.boosters_reseter.cancel()

    @commands.slash_command(description=_("inventory-desc"))
    async def inventory(
        self,
        interaction: disnake.GuildCommandInteraction,
    ) -> None:
        guild = interaction.guild
        user = interaction.user

        inventory = await get_inventory(guild.id, user.id)
        view = InventoryCategoriesView(inventory)

        await view.start(interaction, {"inventory": inventory})

    @tasks.loop(minutes=1)
    async def boosters_reseter(self) -> None:
        for guild in self.bot.guilds:
            users = await reset_boosters(guild.id)
            if users: logger.debug(
                "У пользователей [%s] закончилось действие усилителя опыта",
                ", ".join([f"<@{user}>" for user in users]),
                extra={
                    "user_avatar": user_avatar(jester=True),
                    "type": "else",
                    "guild_id": guild.id
                })
