import abc
import uuid
from dataclasses import dataclass, field


@dataclass
class BaseEvent(abc.ABC):
    id: uuid.UUID = field(default_factory=lambda: uuid.uuid4(), kw_only=True)

