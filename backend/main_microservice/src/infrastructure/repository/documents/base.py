from dataclasses import dataclass
from abc import ABC, abstractmethod

from motor.core import AgnosticCollection

from domain.entities.document import Document
from domain.entities.version import Version


@dataclass
class BaseDocumentRepository(ABC):
    @abstractmethod
    async def add_new_version(self, document_name: str, version: Version, user_id: int) -> None: ...
    @abstractmethod
    async def get_last_version(self, document_name: str, user_id: int) -> Version | None: ...
    @abstractmethod
    async def delete_answers(self, document_name: str, user_id: int) -> None: ...
