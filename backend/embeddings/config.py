from pydantic_settings import BaseSettings
from pydantic import Field


class APISettings(BaseSettings):
    port: int = Field(alias="EMB_API_PORT", default=8000)


class Settings(BaseSettings):
    model_name: str = "deepvk/USER-bge-m3"
    device_index: int
    api: APISettings = APISettings()


settings = Settings()
