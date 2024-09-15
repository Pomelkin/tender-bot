import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InputFile, FSInputFile
from fastapi import HTTPException

from routers.conversation.callback_data import DocTypeData
from routers.conversation.fsm import Document
from routers.conversation.keyboards import get_choose_doc_type_keyboard, get_generate_keyboard
from routers.conversation.schemas import Resolution, ShowDiff
from routers.conversation.utils import create_pdf

from routers.conversation.requests import send_user_query, send_create_agreement

router = Router()


@router.message(Document.id)
async def get_document_handler(message: types.Message, state: FSMContext):
    await message.answer("Документ найден, напишите свой вопрос или инциализируйте генерацию соглашения",
                         reply_markup=get_generate_keyboard())
    await state.update_data(document_id=message.text)
    await state.set_state(Document.conversation)


@router.message(Document.conversation, F.text.lower() == "сгенерировать соглашение")
async def generate_agreement_handler(message: types.Message, state: FSMContext):
    await message.answer("Напишите структурированное и понятное описание для создания Дополнительного Согласения")
    await state.set_state(Document.create_agreement)


@router.message(Document.conversation)
async def get_conversation_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    document_id = data["document_id"]
    response = await send_user_query({"vault_id": document_id, "query": message.text})
    await message.answer(response["content"])


@router.message(Document.create_agreement)
async def create_agreement_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    document_id = data["document_id"]
    try:
        logging.info(f"Creating agreement for document: {document_id}")
        response = await send_create_agreement({"document_name": document_id,
                                                "message": message.text,
                                                "user_id": message.from_user.id})

        diff = ShowDiff(**response)
        await state.update_data(current_url=diff.current_url)
        url_to_user = f"https://example.com/?url={diff.current_url}"
        await message.answer(f"Ссылка на соглашение:\n{url_to_user}\n\nЕсли все устраивает - конвертируйте в нужный формат",
                             reply_markup=get_choose_doc_type_keyboard())

    except Exception as e:
        logging.error(e, exc_info=True)
        if isinstance(e, HTTPException):
            return await message.answer(f"{e.detail}\n\nПопробуйте еще раз учитывая рекомендации выше!")
        await message.answer("Что-то пошло не так, попробуйте еще раз!")


@router.callback_query(DocTypeData.filter())
async def process_agreement_to_file(query: types.CallbackQuery, callback_data: DocTypeData, state: FSMContext):
    await query.answer()
    data = await state.get_data()
    current_url = data["current_url"]

    if callback_data.type == "pdf":
        create_pdf(current_url)
        input_file = FSInputFile("sample.pdf")
        await query.message.answer_document(input_file)

    # todo: word
