import disnake
from disnake.ext import commands

from src.bot import JesterBot
from src.utils._converters import inter_member
from ._api_interaction import update_member_coins
from src.utils.ui import BaseEmbed
from src.localization import get_localizator
from src.utils._time import current_time

from src.customisation import BANK_NAME, BANK_INDEF_CODE


_ = get_localizator("economy")


class EconomyCog(commands.Cog):
    def __init__(self, bot: JesterBot) -> None:
        self.bot = bot

    @commands.slash_command(description=_("economy-donate_desc"))
    async def donate(
        self,
        interaction: disnake.GuildCommandInteraction,
        member: disnake.Member = commands.Param(
            converter=inter_member, description=_("economy-donate_member_param")),
        amount: int = commands.Param(
            description=_("economy-donate_amount_param")),
        appointment: str = commands.Param(
            description=_("economy-donate_appointment_param"),
            default=_("economy-donate_appointment_param_default"),
            max_length=55)
    ) -> None:
        amount = abs(amount) # amount must be > 0

        guild_id = interaction.guild_id
        payer_id = interaction.author.id
        receiver_id = member.id

        await update_member_coins(guild_id, payer_id, -amount)
        await update_member_coins(guild_id, receiver_id, amount)
        embed = (BaseEmbed(title = _("economy-donate_embed_title"))
            .add_field(name=_("economy-donate_receiver_field"),
                        value=f"<@{receiver_id}>", inline=True)
            .add_field(name=_("economy-donate_payment_account_field"),
                        value=receiver_id, inline=True)
            .add_field(name="\t", value="\t", inline=True)
            .add_field(name=_("economy-donate_payer_field"),
                        value=f"<@{payer_id}>", inline=True)
            .add_field(name=_("economy-donate_payer_adress_field"),
                        value=interaction.guild.name, inline=True)
            .add_field(name="\t", value="\t", inline=True))
        if appointment:
            embed.add_field(name=_("economy-donate_payment_appointment_field"),
                             value=appointment, inline=False)
        (embed
            .add_field(name=_("economy-donate_payment_amount_field"),
                        value=amount, inline=True)
            .add_field(name=_("economy-donate_payment_date_field"),
                        value=disnake.utils.format_dt(current_time(), 'f'), inline=True)
            .add_field(name="\t", value="\t", inline=True)
            .set_footer(text=(f"{_('economy-donate_PJSC_field')} «{BANK_NAME}»"
                        f" | {_('economy-donate_BIC_field')} {BANK_INDEF_CODE}")))
        await interaction.response.send_message(embed=embed)

    # @commands.cooldown(1, 24*60*60, commands.BucketType.user)
    # @commands.slash_command(description=_("economy-daily_desc"))
    # async def daily(
    #     self,
    #     interaction: disnake.GuildCommandInteraction,
    # ) -> None:
    #     from src.config import cfg
    #     guild_id = interaction.guild.id 
    #     user_id = interaction.user.id

    #     daily_bonus = cfg.economy_cfg(guild_id).daily_bonus
        
    #     await update_member_coins(guild_id, user_id, daily_bonus)
    #     await interaction.response.send_message(_("economy-daily_response"))
        