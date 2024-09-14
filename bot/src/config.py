from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: str
    base_url: str

    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str


settings = Settings()