from dataclasses import dataclass

from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class DocumentFile(BaseValueObject):
    value: bytes

    def validate(self):
        ...

    def as_generic_type(self) -> bytes:
        return self.value
