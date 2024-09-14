from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class ConsultationService(ABC):
    host: str
    port: int

    @abstractmethod
    async def get_consultation(self, vector_collection_name: str, message: str) -> str: ...
