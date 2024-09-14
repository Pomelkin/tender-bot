from dataclasses import dataclass
from abc import ABC, abstractmethod

from motor.core import AgnosticCollection

from domain.entities.document import Document
from domain.entities.version import Version


@dataclass
class BaseDocumentRepository(ABC):
    async def get_document_by_id(self, document_id: str, user_id: int) -> Document: ...
    async def get_version(self, document_id: str, version_id: str, user_id: int) -> Version: ...
    async def add_new_version(self, document_id: str, version: Version, user_id: int) -> None: ...
    async def get_last_version(self, document_id: str, user_id: int) -> Version | None: ...
