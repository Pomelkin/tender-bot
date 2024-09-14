import datetime
import uuid
from dataclasses import dataclass, field

from domain.entities.base import BaseEntity


@dataclass
class Version(BaseEntity):
    parent_document_id: uuid.UUID
    number_of_version: int = field(default=1)
    approve: tuple[bool, bool] = field(default_factory=lambda: (False, False))
    timestamp: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.UTC))
