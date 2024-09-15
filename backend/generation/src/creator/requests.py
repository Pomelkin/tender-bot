from aiohttp import ClientSession
from generation.src.config import settings


async def request_rag(document_name: str, message: str) -> str:
    """
    Requests RAG service to generate a document based on the given
    document_name and message.

    Args:
        document_name (str): The name of the document to generate.
        message (str): The message to generate the document based on.

    Returns:
        str: The generated document content.
    """
    async with ClientSession() as client:
        async with client.post(
            f"{settings.rag_service_url}/answer",
            json={"vault_id": f"{document_name}.txt", "query": message},
        ) as response:
            response_json = await response.json()
            return response_json["content"]
