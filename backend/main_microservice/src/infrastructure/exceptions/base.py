from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class InfrastructureException(ApplicationException):
    @property
    def message(self):
        return "В обработке запроса возникла ошибка"