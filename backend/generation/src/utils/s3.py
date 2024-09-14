import io
from contextlib import asynccontextmanager
from io import BytesIO

from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session
from generation.src.config import settings


class S3Repository:
    def __init__(self):
        self.access_key = settings.s3_access_key
        self.secret_key = settings.s3_secret_key
        self.endpoint_url = settings.s3_endpoint_url
        self.bucket_name = settings.s3_bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self) -> AioBaseClient:
        config = {
            "aws_access_key_id": self.access_key,
            "aws_secret_access_key": self.secret_key,
            "endpoint_url": self.endpoint_url,
        }
        async with self.session.create_client("s3", **config) as client:
            yield client

    async def get(self, file_id: str) -> BytesIO:
        async with self.get_client() as client:
            response = await client.get_object(Bucket=self.bucket_name, Key=file_id)
            buffer = io.BytesIO()
            async with response["Body"] as stream:
                data = await stream.read()
                buffer.write(data)
            buffer.seek(0)
            return buffer

    async def put(self, file: bytes, file_id: str) -> None:
        async with self.get_client() as client:
            object_name = str(file_id)
            await client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file,
            )

    async def delete(self, file_id: str):
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=file_id)
