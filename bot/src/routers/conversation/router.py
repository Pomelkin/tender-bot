from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from routers.conversation.callback_data import DocTypeData
from routers.conversation.fsm import Document
from routers.conversation.keyboards import get_choose_doc_type_keyboard, get_generate_keyboard
from routers.conversation.utils import create_pdf

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
    # response = await send_user_query({"document_id": document_id, "query": message.text})
    await message.answer("answer")


@router.message(Document.create_agreement)
async def create_agreement_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    document_id = data["document_id"]
    # response = await send_create_agreement({"document_id": document_id, "query": message.text})
    # resolution = Resolution(**response)

    # if not resolution.status:
    #     return await message.answer(resolution.message + "\n\nПопробуйте еще раз учитывая рекомендации выше")

    await message.answer("\n\nВыберите тип итогового документа", reply_markup=get_choose_doc_type_keyboard())


@router.callback_query(DocTypeData.filter())
async def process_agreement_to_file(query: types.CallbackQuery, callback_data: DocTypeData, state: FSMContext):
    await query.answer()

    if callback_data.type == "pdf":
        create_pdf()
        await query.message.answer_document("sample.pdf")

    # todo: word
