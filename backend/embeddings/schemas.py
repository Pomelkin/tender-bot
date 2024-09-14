from typing import List
from pydantic import BaseModel, Field, ConfigDict


class EmbeddingsRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    input: str | List[str] = Field(description="The input to embed.")


class Embedding(BaseModel):
    object: str = "embedding"
    index: int
    embedding: List[float]


class Usage(BaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0


class EmbeddingsResponse(BaseModel):
    object: str = "list"
    data: List[Embedding]
    model: str = "nyam"
