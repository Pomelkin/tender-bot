from typing import Literal

from aiogram.filters.callback_data import CallbackData


class DocTypeData(CallbackData, prefix="doc_type"):
    type: Literal["pdf", "docx"]
