from abc import ABC
from dataclasses import dataclass
from motor.core import AgnosticClient, AgnosticCollection

from infrastructure.repository.documents.base import BaseDocumentRepository


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str

    def _collection(self, collection_name: str) -> AgnosticCollection:
        return self.mongo_db_client[self.mongo_db_db_name][collection_name]


@dataclass
class MongoDocumentRepository(BaseDocumentRepository, BaseMongoDBRepository):

    def create_new_document(self):