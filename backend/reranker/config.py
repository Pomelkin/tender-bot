from pydantic_settings import BaseSettings
from pydantic import Field


class APISettings(BaseSettings):
    port: int = Field(alias="CROSS_API_PORT", default=8000)


class Settings(BaseSettings):
    model_name: str = "DiTy/cross-encoder-russian-msmarco"
    device_index: int
    rerank_threshold: float = 0.7
    api: APISettings = APISettings()


settings = Settings()
