from generation.src.config import settings
from openai import AsyncOpenAI

client_author = AsyncOpenAI(
    base_url=settings.author_base_url,
    api_key="token-abc123",
)

client_editor = AsyncOpenAI(
    base_url=settings.editor_base_url,
    api_key="token-abc123",
)
