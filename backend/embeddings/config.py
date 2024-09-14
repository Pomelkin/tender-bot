from pydantic_settings import BaseSettings
from pydantic import Field


class APISettings(BaseSettings):
    port: int = Field(alias="EMB_API_PORT", default=8000)
    host: str = Field(alias="EMB_API_HOST", default="localhost")


class Settings(BaseSettings):
    model_name: str = "deepvk/USER-bge-m3"
    api: APISettings = APISettings()


settings = Settings()
