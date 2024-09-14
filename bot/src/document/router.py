from aiogram import Router, types

from document.utils import get_user_documents

router = Router()

@router.message(text="Мои документы")
async def my_document_handler(message: types.Message):
    documents = await get_user_documents(user_id=message.from_user.id)