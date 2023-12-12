import logging

from aiogram import Router, F
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import Message, ErrorEvent
from fluent.runtime import FluentLocalization

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.error(ExceptionTypeFilter(Exception), F.update.message.as_("message"))
async def handle_my_custom_exception(
    event: ErrorEvent, message: Message, l10n: FluentLocalization
):
    logger.error(f"Critical error caused by {event.exception}", exc_info=True)
    await message.answer(l10n.format_value("error-handler-text"))
