import io
from contextlib import asynccontextmanager
from io import BytesIO

from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session

from domain.entities.version import Version
from infrastructure.s3.base import BaseS3Repository


class S3Repository(BaseS3Repository):
    @asynccontextmanager
    async def _get_client(self) -> AioBaseClient:
        config = {
            "aws_access_key_id": self.access_token,
            "aws_secret_access_key": self.secret_token,
            "endpoint_url": self.endpoint_url,
        }
        async with self.session.create_client("s3", **config, verify=False) as client:
            yield client

    async def _get(self, file_id: str) -> BytesIO:
        async with self._get_client() as client:
            response = await client.get_object(Bucket=self.bucket_name, Key=file_id)
            buffer = io.BytesIO()
            async with response['Body'] as stream:
                data = await stream.read()
                buffer.write(data)
            buffer.seek(0)
            return buffer

    async def _put(self, file: bytes, file_id: str) -> None:
        async with self._get_client() as client:
            object_name = str(file_id)
            await client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file,

            )

    async def _delete(self, file_id: str):
        async with self._get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=file_id)

    async def upload_new_version(self, version: Version) -> None:
        await self._put(version.version.as_bytes(), file_id=str(version.id) + '.html')


