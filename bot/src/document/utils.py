from document.requests import send_check_documents
from document.schemas import Documents


async def get_user_documents(user_id: int):
    response = await send_check_documents({"user_id": user_id})
    documents = Documents(**response)
    return documents
