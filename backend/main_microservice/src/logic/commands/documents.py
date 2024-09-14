from dataclasses import dataclass

from domain.entities.document import Document
from domain.entities.version import Version

from infrastructure.integration.consultation.base import ConsultationService
from infrastructure.integration.document_generation.base import DocumentGeneration
from infrastructure.repository.documents.base import BaseDocumentRepository
from infrastructure.s3.base import BaseS3Repository
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class Consulate(BaseCommand):
    document_id: str
    message: str


@dataclass(frozen=True)
class ConsulateHandler(CommandHandler[Consulate, str]):
    consultation_service: ConsultationService

    async def handle(self, command: Consulate) -> str:
        return await self.consultation_service.get_consultation(vector_collection_name=command.document_id,
                                                                message=command.message)


@dataclass(frozen=True)
class GenerateDocument(BaseCommand):
    user_id: int
    document_id: str
    message: str


@dataclass(frozen=True)
class GenerateDocumentHandler(CommandHandler[GenerateDocument, Version]):
    document_repository: BaseDocumentRepository
    document_generation: DocumentGeneration
    s3: BaseS3Repository

    async def handle(self, command: GenerateDocument) -> Version:
        prev_version = await self.document_repository.get_last_version(document_id=command.document_id, user_id=command.user_id)

        if not prev_version:
            new_version = await self.document_generation.generate_document_with_prev_version(command.document_id, message=command.message, prev_version_url=prev_version.version_url)
            return new_version
        else:
            new_version = await self.document_generation.generate_document(document_id=command.document_id, message=command.message)

        await self.s3.upload_new_version(new_version)
        await self.document_repository.add_new_version(document_id=command.document_id, version=new_version, user_id=command.user_id)
        return new_version
