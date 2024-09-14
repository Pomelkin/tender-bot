import datetime
import uuid
from dataclasses import dataclass, field

from domain.entities.base import BaseEntity


@dataclass
class Version(BaseEntity):
    parent_document_id: uuid.UUID
    version_url: str
    timestamp: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.UTC))
