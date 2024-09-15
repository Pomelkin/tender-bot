import uuid
from dataclasses import dataclass, field
from typing import Literal

from domain.entities.base import BaseEntity
from domain.entities.version import Version


@dataclass
class Document(BaseEntity):
    document_name: str
    telegram_id: int
    versions: set[Version] = field(default_factory=set, kw_only=True)

    @classmethod
    def create_new_document(cls, document_name: str, telegram_id: int) -> "Document":
        return cls(document_name=document_name, telegram_id=telegram_id)

    def add_new_version(self, version: Version) -> None:
        self.versions.add(version)
