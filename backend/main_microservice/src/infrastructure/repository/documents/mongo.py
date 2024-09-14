from abc import ABC
from dataclasses import dataclass
from motor.core import AgnosticClient, AgnosticCollection, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from domain.entities.document import Document
from domain.entities.user import User
from infrastructure.repository.documents.base import BaseDocumentRepository


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str

    def _db(self) -> AgnosticDatabase:
        return self.mongo_db_client[self.mongo_db_db_name]

    def _collection(self, collection_name: str) -> AgnosticCollection:
        return self.mongo_db_client[self.mongo_db_db_name][collection_name]


@dataclass
class MongoDocumentRepository(BaseDocumentRepository, BaseMongoDBRepository):

    async def create_new_document(self, document: Document, customer: User, performer: User) -> AgnosticCollection:
        return await self._db().create_collection(name=str(document.id), customer=customer.telegram_id, performer=performer.telegram_id)


if __name__ == '__main__':
    rep = MongoDocumentRepository(AsyncIOMotorClient(host="localhost", port=27017), "documents")
    print(rep)