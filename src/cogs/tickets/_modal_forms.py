from disnake import MessageCommandInteraction, TextInputStyle

from src.localization import get_localizator
from .classes import ThreadClassification
from src.utils.ui import ModalTextInput, BaseModal
from ._utils import ticket


_ = get_localizator("tickets-modals")


async def support_modal_form(interaction: MessageCommandInteraction):
    question = ModalTextInput(
        label=_("tickets_problem_desc"),
        placeholder=_("tickets_problem_placeholder"),
        style=TextInputStyle.long
    )
    data = await BaseModal(
        _("tickets_support_question"),
        components=[question],
        interaction=interaction
    ).receive_data()
    await ticket(data, ThreadClassification.SUPPORT)
    

async def moderator_modal_form(interaction: MessageCommandInteraction):
    problem = ModalTextInput(
        label=_("tickets_problem_desc"),
        placeholder=_("tickets_problem_placeholder"),
        style=TextInputStyle.long
    )
    # offender = ModalTextInput(
    #     label=_("offender_id"),
    #     placeholder=_("offender_placeholder"),
    #     required=False
    # )
    data = await BaseModal(
        _("tickets_moderation_offense"),
        components=[problem],
        interaction=interaction
    ).receive_data()
    await ticket(data, ThreadClassification.MODERATOR)


async def bot_modal_form(interaction: MessageCommandInteraction):
    problem = ModalTextInput(
        label=_("tickets_problem_desc"),
        placeholder=_("tickets_problem_placeholder"),
        style=TextInputStyle.long
    )
    # command = ModalTextInput(
    #     label=_("command_name"),
    #     placeholder=_("command_placeholder"),
    #     required=False
    # )
    data = await BaseModal(
        _("tickets_bot_issue"),
        components=[problem],
        interaction=interaction,
    ).receive_data()
    await ticket(data, ThreadClassification.DEVELOPER)


async def solution_modal_form(interaction: MessageCommandInteraction):
    solution = ModalTextInput(
        label=_("tickets_solution_text"),
        style=TextInputStyle.long
    )
    data = await BaseModal(
        _("tickets_solution"),
        components=[solution],
        interaction=interaction
    ).receive_data()
    return data
    
