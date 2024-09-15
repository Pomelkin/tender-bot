from dataclasses import dataclass

from domain.entities.document import Document
from domain.entities.version import Version

from infrastructure.integration.consultation.base import ConsultationService
from infrastructure.integration.document_generation.base import BaseDocumentGeneration
from infrastructure.repository.documents.base import BaseDocumentRepository
from infrastructure.s3.base import BaseS3Repository
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class Consulate(BaseCommand):
    document_name: str
    message: str


@dataclass(frozen=True)
class ConsulateHandler(CommandHandler[Consulate, str]):
    consultation_service: ConsultationService

    async def handle(self, command: Consulate) -> str:
        return await self.consultation_service.get_consultation(vector_collection_name=command.document_name,
                                                                message=command.message)


@dataclass(frozen=True)
class GenerateDocument(BaseCommand):
    user_id: int
    document_name: str
    message: str


@dataclass(frozen=True)
class GenerateDocumentHandler(CommandHandler[GenerateDocument, Version]):
    document_repository: BaseDocumentRepository
    document_generation: BaseDocumentGeneration
    s3: BaseS3Repository

    async def handle(self, command: GenerateDocument) -> tuple[Version, Version]:
        prev_version = await self.document_repository.get_last_version(document_name=command.document_name, user_id=command.user_id)
        new_version = await self.document_generation.generate_document(document_name=command.document_name, message=command.message)
        await self.s3.upload_new_version(version=new_version)
        new_version.version = self.s3.create_get_url(file_name=str(new_version.id) + ".html")
        await self.document_repository.add_new_version(document_name=command.document_name, version=new_version, user_id=command.user_id)
        print(new_version, prev_version)
        return new_version, prev_version
