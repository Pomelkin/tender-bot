from dataclasses import dataclass
from aiohttp import ClientSession

from domain.entities.version import Version
from infrastructure.integration.document_generation.base import BaseDocumentGeneration
from infrastructure.exceptions.document_generation import RefusalDocumentGenerationException


@dataclass
class DocumentGeneration(BaseDocumentGeneration):
    async def generate_document(self, document_name: str, message: str) -> Version:
        async with ClientSession() as client:
            async with client.post(f"http://{self.host}:{self.port}/create", json={"document_name": document_name, "query": message}) as response:
                if not response.ok:
                    raise RefusalDocumentGenerationException(text=await response.text())
                return Version.create_from_bytes_html(parent_document_name=document_name, version=await response.content.read())

    async def generate_document_with_prev_version(self, document_id: str, message: str,
                                                  prev_version_url: str) -> Version:
        pass

