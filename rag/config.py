from pydantic_settings import BaseSettings
from pydantic import Field


class QdrantSettings(BaseSettings):
    host: str = Field(alias="QDRANT_HOST")
    port: int = Field(alias="QDRANT_PORT")


class OpenAIEmbeddingsSettings(BaseSettings):
    api_key: str = "bibka"
    host: str = Field(alias="OPENAI_HOST")
    port: int = Field(alias="OPENAI_PORT")


class Gemma2Settings(BaseSettings):
    host: str = Field(alias="GEMMA2_HOST")
    port: int = Field(alias="GEMMA2_PORT")


class RerankerSettings(BaseSettings):
    host: str = Field(alias="RERANKER_HOST")
    port: int = Field(alias="RERANKER_PORT")


class Settings(BaseSettings):
    qdrant: QdrantSettings = QdrantSettings()
    embeddings: OpenAIEmbeddingsSettings = OpenAIEmbeddingsSettings()
    reranker: RerankerSettings = RerankerSettings()
    gemma2: Gemma2Settings = Gemma2Settings()


settings = Settings()
