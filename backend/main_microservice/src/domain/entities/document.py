from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.entities.user import User
from domain.entities.version import Version
from domain.values.document import DocumentFile
from domain.values.file_type import FileType


@dataclass
class Document(BaseEntity):
    document: DocumentFile
    file_type: FileType
    customer: User
    performer: User
    versions: set[Version] = field(default_factory=set, kw_only=True)

    @classmethod
    def create_new_document(cls, document: DocumentFile, file_type: FileType, first_user: User, second_user: User) -> "Document":
        return cls(document=document, file_type=file_type, customer=first_user, performer=second_user)

    def add_new_version(self, version: Version) -> None:
        self.versions.add(version)

