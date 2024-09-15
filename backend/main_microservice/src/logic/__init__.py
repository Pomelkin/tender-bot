from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from infrastructure.integration.document_generation.base import BaseDocumentGeneration
from infrastructure.integration.document_generation.document_generation import DocumentGeneration
from infrastructure.repository.documents.base import BaseDocumentRepository
from infrastructure.repository.documents.mongo import MongoDocumentRepository
from infrastructure.s3.base import BaseS3Repository
from infrastructure.s3.s3 import S3Repository
from logic.commands.documents import GenerateDocumentHandler, GenerateDocument, UploadNewVersionHandler, \
    UploadNewVersion
from logic.mediator import Mediator
from config.config import Settings


@lru_cache(1)
def _init_container():
    return _init_container()


@lru_cache(None)
def init_container():
    container = Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)

    def init_mediator():
        mediator = Mediator()

        container.register(GenerateDocumentHandler)
        container.register(UploadNewVersionHandler)

        mediator.register_command(GenerateDocument, [container.resolve(GenerateDocumentHandler)])
        mediator.register_command(UploadNewVersion, [container.resolve(UploadNewVersionHandler)])

        return mediator

    def init_document_repository():
        config: Settings = container.resolve(Settings)
        return MongoDocumentRepository(AsyncIOMotorClient(host=config.mongodb_host, port=config.mongodb_port), config.mongodb_name)

    container.register(BaseDocumentRepository, init_document_repository, scope=Scope.singleton)

    def init_s3_repository():
        config: Settings = container.resolve(Settings)
        return S3Repository(endpoint_url=config.s3_host, access_token=config.s3_access_token, bucket_name="tender-bot", secret_token=config.s3_secret_token, endpoint_get_url=config.s3_endpoint_get_url)

    container.register(BaseS3Repository, init_s3_repository, scope=Scope.singleton)

    def init_document_generation() -> BaseDocumentGeneration:
        config: Settings = container.resolve(Settings)
        return DocumentGeneration(host=config.generation_document_host, port=config.generation_document_port)

    container.register(BaseDocumentGeneration, factory=init_document_generation, scope=Scope.singleton)

    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)

    return container
