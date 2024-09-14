from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class InvalidS3URLException(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return f"Неверный формат url для s3 {self.text}"
