from dataclasses import dataclass, field
from typing import Literal

from domain.entities.base import BaseEntity
from domain.entities.version import Version


@dataclass
class Document(BaseEntity):
    telegram_id: int
    file_type: Literal['pdf', 'docx']
    versions: set[Version] = field(default_factory=set, kw_only=True)

    @classmethod
    def create_new_document(cls, file_type: Literal['pdf', 'docx'], telegram_id: int) -> "Document":
        return cls(file_type=file_type, telegram_id=telegram_id)

    def add_new_version(self, version: Version) -> None:
        self.versions.add(version)
