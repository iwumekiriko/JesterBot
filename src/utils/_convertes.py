import disnake
from disnake.ext import commands

from src.localization import get_localizator


_ = get_localizator()


def _member(
    inter: disnake.ApplicationCommandInteraction,
    arg: disnake.User | disnake.Member
) -> disnake.Member:
    if not isinstance(arg, disnake.Member):
        raise commands.BadArgument(_("not_found_member_error"))
    return arg


def bot_excluding(
    inter: disnake.ApplicationCommandInteraction,
    arg: disnake.Member | disnake.User
) -> disnake.Member:
    member = _member(inter, arg)
    if member.bot:
        raise commands.BadArgument(_("not_for_bot_error"))
    return member


def self_excluding(
    inter: disnake.ApplicationCommandInteraction,
    arg: disnake.Member | disnake.User
) -> disnake.Member:
    member = _member(inter, arg)
    if member == inter.user:
        raise commands.BadArgument(_("not_for_self_error"))
    return member


def owner_excluding(
    inter: disnake.ApplicationCommandInteraction,
    arg: disnake.Member | disnake.User
) -> disnake.Member:
    member = _member(inter, arg)
    if member.id == 567303956448018456:
        raise commands.BadArgument(_("not_for_owner_error"))
    return member


def inter_member(
    inter: disnake.ApplicationCommandInteraction,
    arg: disnake.Member | disnake.User
) -> disnake.Member:
    _not_bot = bot_excluding(inter, arg)
    _not_self_nor_bot = self_excluding(inter, _not_bot)
    _not_self_nor_bot_nor_owner = owner_excluding(
        inter, _not_self_nor_bot)
    return _not_self_nor_bot_nor_owner


def user_avatar(user_id: int = 0, jester: bool = False) -> str | None:
    from src.bot import bot
    if user_id == 0 and not jester: return None 

    return (bot.get_user(user_id).display_avatar.url or None # type: ignore
        if not jester else bot.user.avatar.url) # type: ignore