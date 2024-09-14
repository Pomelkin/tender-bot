import uuid
from dataclasses import dataclass
from abc import ABC, abstractmethod

from domain.entities.version import Version


@dataclass
class BaseS3Repository(ABC):
    host: str
    port: int

    @abstractmethod
    async def upload_new_version(self, version: Version) -> None: ...
    @abstractmethod
    async def get_version(self, version_id: uuid.UUID) -> Version: ...