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

    async def add_new_version(self, document_name: str, version: Version, user_id: int) -> None:
        await self._collection(self._generate_collection_name(document_name, user_id)).insert_one(version.model_dump())

    async def get_last_version(self, document_name: str, user_id: int) -> Version | None:
        version = await self._collection(self._generate_collection_name(document_name, user_id)).find_one(sort=[("_id", -1)])
        if version:
            return convert_version_mongo_to_entity(version=version)
        return

    async def delete_answers(self, document_name: str, user_id: int) -> None:
        await self._collection(self._generate_collection_name(document_name, user_id)).drop()
