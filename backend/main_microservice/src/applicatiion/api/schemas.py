from pydantic import BaseModel

from domain.entities.version import Version


class ErrorSchema(BaseModel):
    error: str


class GenerateDocumentRequestSchema(BaseModel):
    user_id: int
    document_name: str
    message: str


class GenerateDocumentResponseSchema(BaseModel):
    version_url: str

    @classmethod
    def from_entity(cls, version: Version):
        return cls(version_url=version.version)
