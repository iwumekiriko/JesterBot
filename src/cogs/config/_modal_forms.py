from disnake import MessageCommandInteraction, TextInputStyle
from typing import Any, Dict, List, Sequence, Union

from src.localization import get_localizator
from src.utils.ui import ModalTextInput, BaseModal, ModalLabel, ModalTextDisplay
from ._api_interaction import set_local_cfg
from src.models.config import *


_ = get_localizator("config.modals")


FIELDS_PER_PAGE = 5
EXCLUDING = "excluding"


async def experience_cfg_modal_form(
    interaction: MessageCommandInteraction,
    base_exp_for_message: int | None = 3,
    base_exp_for_voice_minute: int | None = 1,
    page: int = 0
):
    exp_for_message = ModalLabel(
        text=_("exp_for_message_input"),
        key="exp_for_message",
        component=ModalTextInput(
            value=str(base_exp_for_message),
            required=False
    ))
    exp_for_voice_minute = ModalLabel(
        text=_("exp_for_voice_minute_input"),
        key="exp_for_voice_minute",
        component=ModalTextInput(
            value=str(base_exp_for_voice_minute),
            required=False
    ))
    components_data = [exp_for_message, exp_for_voice_minute]
    components = _page_components(components_data, page)
    data = await BaseModal(
        _("experience_cfg_modal"),
        components=components,
        interaction=interaction
    ).receive_data()
    await set_local_cfg(_make_data(components, data), ExperienceConfig)
    return data[0]


async def roles_cfg_modal_form(
    interaction: MessageCommandInteraction,
    base_support_role_id: int | None = 0,
    base_moderator_role_id: int | None = 0,
    base_developer_role_id: int | None = 0,
    page: int = 0
):
    support_role_id = ModalLabel(
        text=_("support_role_id_input"),
        key="support_role_id",
        component = ModalTextInput(
            value=str(base_support_role_id),
            required=False
        ))
    moderator_role_id = ModalLabel(
        text=_("moderator_role_id_input"),
        key="moderator_role_id",
        component = ModalTextInput(
            value=str(base_moderator_role_id),
            required=False
        ))
    developer_role_id = ModalLabel(
        text=_("developer_role_id_input"),
        key="developer_role_id",
        component=ModalTextInput(
            value=str(base_developer_role_id),
            required=False
    ))
    components_data = [support_role_id, moderator_role_id, developer_role_id]
    components = _page_components(components_data, page)
    data = await BaseModal(
        _("roles_cfg_modal"),
        components=components,
        interaction=interaction
    ).receive_data()
    await set_local_cfg(_make_data(components, data), RolesConfig)
    return data[0]


async def channels_cfg_modal_form(
    interaction: MessageCommandInteraction,
    base_general_channel_id: int | None = 0,
    base_offtop_channel_id: int | None = 0,
    base_nitro_boosting_channel_id: int | None = 0,
    base_image_saver_channel_id: int | None = 0,
    page: int = 0
):
    general_channel_id = ModalLabel(
        text=_("general_channel_id_input"),
        key="general_channel_id",
        component=ModalTextInput(
            value=str(base_general_channel_id),
            required=False
        ))

    offtop_channel_id = ModalLabel(
        text=_("offtop_channel_id_input"),
        key="offtop_channel_id",
        component=ModalTextInput(
            value=str(base_offtop_channel_id),
            required=False
        ))

    nitro_boosting_channel_id = ModalLabel(
        text=_("nitro_boosting_channel_id_input"),
        key="nitro_boosting_channel_id",
        component=ModalTextInput(
            value=str(base_nitro_boosting_channel_id),
            required=False
        ))
    
    image_saver_channel_id = ModalLabel(
        text=_("image_saver_channel_id_input"),
        key="image_saver_channel_id",
        component=ModalTextInput(
            value=str(base_image_saver_channel_id),
            required=False
        )
    )

    components_data = [
        general_channel_id,
        offtop_channel_id,
        nitro_boosting_channel_id,
        image_saver_channel_id
    ]
    components = _page_components(components_data, page)
    data = await BaseModal(
        _("channels_cfg_modal"),
        components=components,
        interaction=interaction
    ).receive_data()
    await set_local_cfg(_make_data(components, data), ChannelsConfig)
    return data[0]


async def shop_cfg_modal_form(
    interaction: MessageCommandInteraction,
    base_shop_channel_id: int | None = 0,
    base_shop_message_id: int | None = 0,
    page: int = 0
):
    shop_channel_id = ModalLabel(
        text=_("shop_channel_id_input"),
        key="shop_channel_id",
        component=ModalTextInput(
            value=str(base_shop_channel_id),
            required=False
        ))

    shop_message_id = ModalLabel(
        text=_("shop_message_id_input"),
        key="shop_message_id",
        component=ModalTextInput(
            value=str(base_shop_message_id),
            required=False
        ))

    components_data = [
        shop_channel_id,
        shop_message_id
    ]

    components = _page_components(components_data, page)
    data = await BaseModal(
        _("shop_cfg_modal"),
        components=components,
        interaction=interaction
    ).receive_data()
    await set_local_cfg(_make_data(components, data), ShopConfig)
    return data[0]


async def tickets_cfg_modal_form(
    interaction: MessageCommandInteraction,
    base_ticket_channel_id: int | None = 0,
    base_ticket_message_id: int | None = 0,
    base_ticket_report_channel_id: int | None = 0,
    page: int = 0
):
    ticket_channel_id = ModalLabel(
        text=_("ticket_channel_id_input"),
        key="ticket_channel_id",
        component=ModalTextInput(
            value=str(base_ticket_channel_id),
            required=False
        ))

    ticket_message_id = ModalLabel(
        text=_("ticket_message_id_input"),
        key="ticket_message_id",
        component=ModalTextInput(
            value=str(base_ticket_message_id),
            required=False
        ))

    ticket_report_channel_id = ModalLabel(
        text=_("ticket_report_channel_id_input"),
        key="ticket_report_channel_id",
        component=ModalTextInput(
            value=str(base_ticket_report_channel_id),
            required=False
        ))

    components_data = [
        ticket_channel_id,
        ticket_message_id,
        ticket_report_channel_id
    ]

    components = _page_components(components_data, page)
    data = await BaseModal(
        _("tickets_cfg_modal"),
        components=components,
        interaction=interaction
    ).receive_data()
    await set_local_cfg(_make_data(components, data), TicketsConfig)
    return data[0]


async def voice_cfg_modal_form(
    interaction: MessageCommandInteraction,
    base_custom_voice_creation_channel_id: int | None = 0,
    base_custom_voice_category_id: int | None = 0,
    base_custom_voice_deletion_time: int | None = 30,
    page: int = 0
):
    custom_voice_creation_channel_id = ModalLabel(
        text=_("custom_voice_creation_channel_id_input"),
        key="custom_voice_creation_channel_id",
        component=ModalTextInput(
            value=str(base_custom_voice_creation_channel_id),
            required=False
        ))

    custom_voice_category_id = ModalLabel(
        text=_("custom_voice_category_id_input"),
        key="custom_voice_category_id",
        component=ModalTextInput(
            value=str(base_custom_voice_category_id),
            required=False
        ))

    custom_voice_deletion_time = ModalLabel(
        text=_("custom_voice_deletion_time_input"),
        key="custom_voice_deletion_time",
        component=ModalTextInput(
            value=str(base_custom_voice_deletion_time),
            required=False
        ))

    components_data = [
        custom_voice_creation_channel_id,
        custom_voice_category_id,
        custom_voice_deletion_time
    ]

    components = _page_components(components_data, page)
    data = await BaseModal(
        _("voice_cfg_modal"),
        components=components,
        interaction=interaction
    ).receive_data()
    await set_local_cfg(_make_data(components, data), VoiceConfig)
    return data[0]


async def logs_cfg_modal_form(
    interaction: MessageCommandInteraction,
    base_command_interactions_webhook_url: str | None = "",
    base_messages_webhook_url: str | None = "",
    base_tickets_webhook_url: str | None = "",
    base_guild_webhook_url: str | None = "",
    base_members_webhook_url: str | None = "",
    base_voice_webhook_url: str | None = "",
    base_else_webhook_url: str | None = "",
    page: int = 0
):
    command_interactions_webhook_url = ModalLabel(
        text=_("command_interactions_webhook_url_input"),
        key="command_interactions_webhook_url",
        component=ModalTextInput(
            value=str(base_command_interactions_webhook_url),
            style=TextInputStyle.long,
            required=False
        ))

    messages_webhook_url = ModalLabel(
        text=_("messages_webhook_url_input"),
        key="messages_webhook_url",
        component=ModalTextInput(
            value=str(base_messages_webhook_url),
            style=TextInputStyle.long,
            required=False
        ))

    tickets_webhook_url = ModalLabel(
        text=_("tickets_webhook_url_input"),
        key="tickets_webhook_url",
        component=ModalTextInput(
            value=str(base_tickets_webhook_url),
            style=TextInputStyle.long,
            required=False
        ))

    guild_webhook_url = ModalLabel(
        text=_("guild_webhook_url_input"),
        key="guild_webhook_url",
        component=ModalTextInput(
            value=str(base_guild_webhook_url),
            style=TextInputStyle.long,
            required=False
        ))

    members_webhook_url = ModalLabel(
        text=_("members_webhook_url_input"),
        key="members_webhook_url",
        component=ModalTextInput(
            value=str(base_members_webhook_url),
            style=TextInputStyle.long,
            required=False
        ))

    voice_webhook_url = ModalLabel(
        text=_("voice_webhook_url_input"),
        key="voice_webhook_url",
        component=ModalTextInput(
            value=str(base_voice_webhook_url),
            style=TextInputStyle.long,
            required=False
        ))

    else_webhook_url = ModalLabel(
        text=_("else_webhook_url_input"),
        key="else_webhook_url",
        component=ModalTextInput(
            value=str(base_else_webhook_url),
            style=TextInputStyle.long,
            required=False
        ))

    components_data = [
        command_interactions_webhook_url,
        messages_webhook_url,
        tickets_webhook_url,
        guild_webhook_url,
        members_webhook_url,
        voice_webhook_url,
        else_webhook_url
    ]

    components = _page_components(components_data, page)
    data = await BaseModal(
        _("logs_cfg_modal"),
        components=components,
        interaction=interaction
    ).receive_data()
    await set_local_cfg(_make_data(components, data), LogsConfig)
    return data[0]


async def lootboxes_cfg_modal_form(
    interaction: MessageCommandInteraction,
    base_roles_lootbox_key_price: int | None = 0,
    base_backgrounds_lootbox_key_price: int | None = 0,
    base_active_lootboxes: list[str] | None = None,
    page: int = 0
):
    roles_lootbox_keys_price = ModalLabel(
        text=_("roles_lootbox_key_price_input"),
        key="roles_lootbox_key_price",
        component=ModalTextInput(
            value=str(base_roles_lootbox_key_price),
            required=False
        ))

    backgrounds_lootbox_keys_price = ModalLabel(
        text=_("backgrounds_lootbox_key_price_input"),
        key="backgrounds_lootbox_key_price",
        component=ModalTextInput(
            value=str(base_backgrounds_lootbox_key_price),
            required=False
        ))

    active_lootboxes = ModalLabel(
        text=_("active_lootboxes_input"),
        key="active_lootboxes",
        component=ModalTextInput(
            value=str(base_active_lootboxes),
            style=TextInputStyle.long,
            required=False
        ))

    from src.cogs.lootboxes._lootbox_map import LootboxMap
    active_lootboxes_tip = ModalTextDisplay(
        key=None,
        content=_("active_lootboxes_tip_value",
            available=LootboxMap.values()
        )
    )

    components_data = [
        roles_lootbox_keys_price,
        backgrounds_lootbox_keys_price,
        active_lootboxes,
        active_lootboxes_tip
    ]

    components = _page_components(components_data, page)

    data = await BaseModal(
        _("lootboxes_cfg_modal"),
        components=components,
        interaction=interaction
    ).receive_data()

    await set_local_cfg(
        _make_data(components, data),
        LootboxesConfig
    )

    return data[0]


async def economy_cfg_modal_form(
    interaction: MessageCommandInteraction,
    base_default_currency_icon: str | None = "",
    base_donate_currency_icon: str | None = "",
    base_daily_bonus: int | None = 0,
    page: int = 0
):
    default_currency_icon = ModalLabel(
        text=_("default_currency_icon_input"),
        key="default_currency_icon",
        component=ModalTextInput(
            value=base_default_currency_icon,
            required=False
        ))

    donate_currency_icon = ModalLabel(
        text=_("donate_currency_icon_input"),
        key="donate_currency_icon",
        component=ModalTextInput(
            value=base_donate_currency_icon,
            required=False
        ))

    daily_bonus = ModalLabel(
        text=_("daily_bonus_input"),
        key="daily_bonus",
        component=ModalTextInput(
            value=str(base_daily_bonus),
            required=False
        ))

    components_data = [
        default_currency_icon,
        donate_currency_icon,
        daily_bonus
    ]
    components = _page_components(components_data, page)
    data = await BaseModal(
        _("economy_cfg_modal"),
        components=components,
        interaction=interaction
    ).receive_data()
    await set_local_cfg(_make_data(components, data), EconomyConfig)
    return data[0]


async def quests_cfg_modal_form(
    interaction: MessageCommandInteraction,
    base_quests_channel_id: int | None = 0,
    base_quests_message_id: int | None = 0,
    page: int = 0
):
    quests_channel_id = ModalLabel(
        text=_("quests_channel_id_input"),
        key="quests_channel_id",
        component=ModalTextInput(
            value=str(base_quests_channel_id),
            required=False
        ))

    quests_message_id = ModalLabel(
        text=_("quests_message_id_input"),
        key="quests_message_id",
        component=ModalTextInput(
            value=str(base_quests_message_id),
            required=False
        ))

    components_data = [
        quests_channel_id,
        quests_message_id
    ]

    components = _page_components(components_data, page)
    data = await BaseModal(
        _("quests_cfg_modal"),
        components=components,
        interaction=interaction
    ).receive_data()
    await set_local_cfg(_make_data(components, data), QuestsConfig)
    return data[0]


async def packs_cfg_modal_form(
    interaction: MessageCommandInteraction,
    base_packs_price: int | None = 0,
    page: int = 0
):
    packs_price = ModalLabel(
        text=_("packs_price_input"),
        key="packs_price",
        component=ModalTextInput(
            value=str(base_packs_price),
            required=False
        ))

    components_data = [packs_price]
    components = _page_components(components_data, page)
    data = await BaseModal(
        _("packs_cfg_modal"),
        components=components,
        interaction=interaction
    ).receive_data()
    await set_local_cfg(_make_data(components, data), PacksConfig)
    return data[0]


def _make_data(components: Sequence[Union[ModalLabel, ModalTextDisplay]], data: Any) -> Dict:
    values = [
        value if value != "" else None
        for value in data[1:]
    ]

    cfg_data = {
        component.key: value
        for component, value in zip(components, values)
        if component.key is not None
    }
    cfg_data["guild_id"] = data[0].guild.id
    return cfg_data


def _page_components(components: List, page: int) -> List:
    start_index = page * FIELDS_PER_PAGE
    end_index = min(start_index + FIELDS_PER_PAGE, len(components))
    return components[start_index:end_index]