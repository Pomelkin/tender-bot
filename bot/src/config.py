from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: str
    base_url: str


settings = Settings()