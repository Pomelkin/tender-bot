from dataclasses import dataclass
from domain.entities.base import BaseEntity


@dataclass
class User(BaseEntity):
    telegram_id: int
