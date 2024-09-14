import datetime
import uuid
from dataclasses import dataclass, field
from io import BytesIO

from domain.entities.base import BaseEntity
from domain.values.html_version import HTMLVersion
from domain.values.s3_url import S3URL


@dataclass
class Version(BaseEntity):
    parent_document_name: str
    version: S3URL | HTMLVersion
    timestamp: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.UTC))

    @classmethod
    def create_from_bytes_html(cls, parent_document_name: str, version: bytes) -> 'Version':
        buffer = BytesIO()
        buffer.write(version)
        uid = uuid.uuid4()
        buffer.name = str(uid) + ".html"
        buffer.seek(0)
        return cls(id=uid, parent_document_name=parent_document_name, version=HTMLVersion(buffer))
