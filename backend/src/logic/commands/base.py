from dataclasses import dataclass
import abc
from typing import Any


@dataclass(frozen=True)
class BaseCommand(abc.ABC): ...


@dataclass(frozen=True)
class CommandHandler[CT: BaseCommand, CR: Any](abc.ABC):
    @abc.abstractmethod
    async def handle(self, command: CT) -> CR: ...
