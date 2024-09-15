from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: str

    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str

    BASE_URL_GENERATE: str
    BASE_URL_RAG: str
    FRONT_URL: str


settings = Settings()