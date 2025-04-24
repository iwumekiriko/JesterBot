from disnake import Embed

from src.models.inventory_items import Item, Role
from src.models.quests import Quest
from .ui import BaseEmbed
from ._mapping import tabled_, BorderStyle, AlignStyle
from src.customisation import ITEMS_SUMMARY_EMBED_COLOR
from src.utils._time import make_discord_timestamp

from src.localization import get_localizator


_ = get_localizator("cards")


def item_card(item: Item, with_count: bool = True) -> Embed:
    embed = BaseEmbed(
        title = item.translated_name,
        description = item.description,
        color = (int(item.embed_color, 0)
                if item.embed_color else BaseEmbed.color)
    )
    if item.thumbnail:
        embed.set_thumbnail(item.thumbnail)
    if not isinstance(item, Role) and with_count:
        embed.add_field(
            name="",
            value=_('cards-count', count=item.quantity),
            inline=False
        )
    return embed


def items_summary_card(items: list[Item]) -> Embed:
    splitted = {}
    for item in items:
        display_name = item.translated_name
        splitted[display_name] = splitted.get(display_name, 0) + item.quantity

    table = tabled_(
        dict(sorted(splitted.items())),
        headers=(_("cards-table_type"),
                  _("cards-table_count")),
        border_style=BorderStyle.DOUBLE,
        align=AlignStyle.CENTER,
        padding=0
    )

    return BaseEmbed(
        title = _("cards-summary"),
        description = f"```\n{table}\n```",
        color = ITEMS_SUMMARY_EMBED_COLOR
    )


def quests_card(quest: Quest) -> Embed:
    quest_desc = _("cards-quest-composite_desc",
                        title=quest.title,
                        main_desc=quest.description,
                        task_desc=quest.task_desc,
                        reward_desc=quest.reward_string)

    quest_desc += "\n" + (_("cards-quest-completed_field", completed=make_discord_timestamp(quest.completed_at))
            if quest.completed_at else _("cards-quest-deadline_field", deadline=make_discord_timestamp(quest.completable_until)))

    embed = BaseEmbed(
        description = quest_desc,
        color = (int(quest.embed_color, 0)) 
                if quest.embed_color else BaseEmbed.color
    ).set_thumbnail(quest.thumbnail)
    return embed
