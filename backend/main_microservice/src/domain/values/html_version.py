from dataclasses import dataclass
from io import BytesIO

from domain.entities.base import BaseValueObject


@dataclass(frozen=True)
class HTMLVersion(BaseValueObject):
    value: BytesIO

    def validate(self):
        ...

    def as_generic_type(self) -> str:
        return self.value.read().decode("utf-8")

    def as_bytes(self) -> bytes:
        return self.value.read()
