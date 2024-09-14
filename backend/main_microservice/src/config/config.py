from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    mongodb_host: str = Field(alias="MONGODB_HOST")
    mongodb_port: int = Field(alias="MONGODB_PORT")
    mongodb_name: str = Field(alias="MONGODB_NAME")

    generation_document_host: str = Field(alias="GENERATION_DOCUMENT_HOST")
    generation_document_port: int = Field(alias="GENERATION_DOCUMENT_PORT")

    s3_host: str = Field(alias="S3_HOST")
    s3_access_token: str = Field(alias="S3_ACCESS_TOKEN")
    s3_secret_token: str = Field(alias="S3_SECRET_TOKEN")
    s3_endpoint_get_url: str = Field(alias="S3_ENDPOINT_GET_URL")
