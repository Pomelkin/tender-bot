from dataclasses import dataclass
from abc import ABC, abstractmethod

from domain.entities.version import Version


@dataclass
class BaseDocumentGeneration(ABC):
    host: str
    port: int

    @abstractmethod
    async def generate_document_with_prev_version(self, document_id: str, message: str, prev_version_url: str) -> Version: ...
    @abstractmethod
    async def generate_document(self, document_name: str, message: str) -> Version: ...
