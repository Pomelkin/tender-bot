from dataclasses import dataclass
from typing import Literal

from domain.exceptions.file_type import IncorrectFileTypeException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class FileType(BaseValueObject):
    value: Literal['pdf', 'docx', 'txt']

    def validate(self):
        if self.value not in ['pdf', 'docx', 'txt']:
            raise IncorrectFileTypeException(self.value)

    def as_generic_type(self) -> str:
        return self.value
