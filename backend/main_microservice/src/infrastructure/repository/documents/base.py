from dataclasses import dataclass
from abc import ABC, abstractmethod

from motor.core import AgnosticCollection

from domain.entities.document import Document
from domain.entities.user import User


@dataclass
class BaseDocumentRepository(ABC):
    def add_new_document(self, document: Document, customer: User, performer: User) -> AgnosticCollection: ...
