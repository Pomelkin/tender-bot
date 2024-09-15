import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from io import BytesIO

from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session, AioSession

from domain.entities.version import Version


@dataclass
class BaseS3Repository(ABC):
    endpoint_url: str
    endpoint_get_url: str
    access_token: str
    secret_token: str
    bucket_name: str
    session: AioSession = field(default_factory=get_session)

    @abstractmethod
    @asynccontextmanager
    async def _get_client(self) -> AioBaseClient: ...

    @abstractmethod
    async def _get(self, file_id: str) -> BytesIO: ...

    @abstractmethod
    async def _put(self, file: bytes, file_id: str) -> None: ...

    @abstractmethod
    async def _delete(self, file_id: str): ...

    @abstractmethod
    async def upload_new_version(self, version: Version) -> str: ...

    def create_get_url(self, file_name: str) -> str:
        return f"{self.endpoint_get_url}/{file_name}"
