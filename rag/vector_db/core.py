from qdrant_client import AsyncQdrantClient
from rag.config import settings

qdrant_instance = AsyncQdrantClient(
    f"http://{settings.qdrant.host}/", port=settings.qdrant.port
)
