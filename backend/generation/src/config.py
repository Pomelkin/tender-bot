from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    editor_base_url: str = Field(
        default="http://pomelk1n-dev.su:8000/v1",
    )
    author_base_url: str = Field(
        default="http://pomelk1n-dev.su:8001/v1",
    )
    s3_access_key: str
    s3_secret_key: str
    s3_endpoint_url: str
    s3_bucket_name: str


settings = Settings()
