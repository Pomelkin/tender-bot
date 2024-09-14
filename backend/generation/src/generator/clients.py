from openai import OpenAI

from generation.src.config import settings

client_author = OpenAI(
    base_url=settings.author_base_url,
    api_key="token-abc123",
)

client_editor = OpenAI(
    base_url=settings.editor_base_url,
    api_key="token-abc123",
)
