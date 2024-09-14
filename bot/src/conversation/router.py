from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from conversation.fsm import Document
from conversation.requests import send_user_query, send_create_agreement
from conversation.schemas import Resolution

router = Router()


@router.message(Document.id)
async def get_document_handler(message: types.Message, state: FSMContext):
    await state.update_data(document_id=message.text)
    await state.set_state(Document.conversation)


@router.message(Document.conversation)
async def get_conversation_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    document_id = data["document_id"]
    response = await send_user_query({"document_id": document_id, "query": message.text})
    await message.answer(response["answer"])


@router.message(text="Сгенерировать соглашение")
async def generate_agreement_handler(message: types.Message, state: FSMContext):
    await message.answer("Напишите структурированное и понятное описание для создания Дополнительного Согласения")
    await state.set_state(Document.create_agreement)


@router.message(Document.create_agreement)
async def create_agreement_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    document_id = data["document_id"]
    response = await send_create_agreement({"document_id": document_id, "query": message.text})
    resolution = Resolution(**response)

    if not resolution.status:
        return await message.answer(resolution.message + "\n\nПопробуйте еще раз учитывая рекомендации выше")

    await message.answer(resolution.message + "\n\nВыберите тип итогового документа", reply_markup=...)
