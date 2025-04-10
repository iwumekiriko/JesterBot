from disnake import Embed

from src.models.inventory_items import Item, Role
from .ui import BaseEmbed
from ._mapping import tabled_, BorderStyle, AlignStyle
from src.customisation import ITEMS_SUMMARY_EMBED_COLOR

from src.localization import get_localizator


_ = get_localizator("items-config")


def item_card(item: Item, with_count: bool = True) -> Embed:
    embed = BaseEmbed(
        title = _(f"items-config-{item.name_lower}_name"),
        description = item.description,
        color = (int(item.embed_color, 0)
                if item.embed_color else BaseEmbed.color)
    )
    if item.thumbnail:
        embed.set_thumbnail(item.thumbnail)
    if not isinstance(item, Role) and with_count:
        embed.add_field(
            name="",
            value=_('items-config-card_count', count=item.quantity),
            inline=False
        )
    return embed


def items_summary_card(items: list[Item]) -> Embed:
    splitted = {}
    for item in items:
        display_name = _(f"items-config-{item.name_lower}_name")
        splitted[display_name] = splitted.get(display_name, 0) + item.quantity

    table = tabled_(
        dict(sorted(splitted.items())),
        headers=(_("items-config-table-type"),
                  _("items-config-table-count")),
        border_style=BorderStyle.DOUBLE,
        align=AlignStyle.CENTER,
        padding=0
    )

    return BaseEmbed(
        title = _("items-config-summary"),
        description = f"```\n{table}\n```",
        color = ITEMS_SUMMARY_EMBED_COLOR
    )
