import asyncio
from abc import ABC
from dataclasses import dataclass
from motor.core import AgnosticClient, AgnosticCollection, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from domain.entities.document import Document
from domain.entities.version import Version
from infrastructure.repository.documents.base import BaseDocumentRepository
from infrastructure.repository.documents.converters import convert_version_mongo_to_entity


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
    @staticmethod
    def _generate_collection_name(document_name: str, user_id: int) -> str:
        return document_name + "_" + str(user_id)

    async def create_new_document(self, document: Document) -> ...:
        await self._db().create_collection(name=str(document.id))

    async def get_document_by_id(self, document_id: str) -> Document:
        document = await self._collection(str(document_id)).find()
        document = Document(document_url=document["document_url"], file_type=document["file_type"], customer=document['customer_id'], performer=document['performer_id'])
        document.versions = [convert_version_mongo_to_entity(version) async for version in self._collection(document_id).find()]
        return document

    async def get_version(self, document_id: str, version_id: str) -> Version:
        return convert_version_mongo_to_entity(version=await self._collection(document_id).find_one({"id": str(version_id)}))

    async def add_new_version(self, document_name: str, version: Version, user_id: int) -> None:
        await self._collection(self._generate_collection_name(document_name, user_id)).insert_one(version.model_dump())

    async def get_last_version(self, document_name: str, user_id: int) -> Version | None:
        version = await self._collection(self._generate_collection_name(document_name, user_id)).find_one(sort=[("_id", -1)])
        if version:
            return convert_version_mongo_to_entity(version=version)
        return


if __name__ == '__main__':
    rep = MongoDocumentRepository(AsyncIOMotorClient(host="localhost", port=27017), "meta", "documents")
    async def main():
        document = Document('sdfd', file_type='pdf', customer=User(123), performer=User(1234))
        version = Version(parent_document_name=document.id, customer_id=document.customer.telegram_id, performer_id=document.performer.telegram_id, version="sfsfsd")
        await rep.create_new_document(document=document)
        await rep.add_new_version(str(document.id), version=version)
        print(await rep.get_document_by_id(str(document.id)))
        print(await rep.get_version(document_id=str(document.id), version_id=str(version.id)))

    asyncio.run(main())