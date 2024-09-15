from dataclasses import dataclass

from infrastructure.exceptions.base import InfrastructureException


@dataclass(frozen=True, eq=False)
class RefusalDocumentGenerationException(InfrastructureException):
    text: str

    @property
    def message(self) -> str:
        return self.text
