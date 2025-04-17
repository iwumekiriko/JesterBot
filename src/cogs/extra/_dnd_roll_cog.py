import random

import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.utils.ui import BaseEmbed


class DNDRollCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self._bot = bot

    @commands.slash_command(description="dnd roll [1, 20]")
    async def roll(
        self,
        interaction: disnake.GuildCommandInteraction
    ) -> None:
        roll = random.randint(1, 20)
        embed=BaseEmbed(
            title="DnD Roll",
            description=f"{interaction.user.mention} rolled: **{roll}**"
        )
        await interaction.response.send_message(embed=embed)