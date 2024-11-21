from disnake import MessageCommandInteraction, TextInputStyle

from src.localization import get_localizator
from .classes._thread_classification import ThreadClassification
from src.utils._modals import ModalTextInput, BaseModal
from ._utils import ticket


_ = get_localizator("modals")


async def support_modal_form(interaction: MessageCommandInteraction):
    question = ModalTextInput(
        label=_("problem_desc"),
        placeholder=_("problem_placeholder"),
        style=TextInputStyle.long
    )
    data = await BaseModal(
        _("support_question"),
        components=[question],
        interaction=interaction
    ).receive_data()
    await ticket(data, ThreadClassification.SUPPORT)
    

async def moderator_modal_form(interaction: MessageCommandInteraction):
    problem = ModalTextInput(
        label=_("problem_desc"),
        placeholder=_("problem_placeholder"),
        style=TextInputStyle.long
    )
    offender = ModalTextInput(
        label=_("offender_id"),
        placeholder=_("offender_placeholder"),
        required=False
    )
    data = await BaseModal(
        _("moderation_offense"),
        components=[problem, offender],
        interaction=interaction
    ).receive_data()
    await ticket(data, ThreadClassification.MODERATOR)


async def bot_modal_form(interaction: MessageCommandInteraction):
    problem = ModalTextInput(
        label=_("problem_desc"),
        placeholder=_("problem_placeholder"),
        style=TextInputStyle.long
    )
    command = ModalTextInput(
        label=_("command_name"),
        placeholder=_("command_placeholder"),
        required=False
    )
    data = await BaseModal(
        _("bot_issue"),
        components=[problem, command],
        interaction=interaction,
    ).receive_data()
    await ticket(data, ThreadClassification.DEVELOPER)


async def solution_modal_form(interaction: MessageCommandInteraction):
    solution = ModalTextInput(
        label=_("solution_text"),
        style=TextInputStyle.long
    )
    data = await BaseModal(
        _("solution"),
        components=[solution],
        interaction=interaction
    ).receive_data()
    return data
    
