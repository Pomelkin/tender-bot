from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class IncorrectFileTypeException(ApplicationException):
    file_type: str

    @property
    def message(self):
        return f"{self.file_type} is not a valid file type"
