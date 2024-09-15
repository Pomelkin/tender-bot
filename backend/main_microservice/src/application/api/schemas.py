from pydantic import BaseModel, Field
from fastapi import Body, File

from domain.entities.version import Version


class ErrorSchema(BaseModel):
    error: str


class GenerateDocumentRequestSchema(BaseModel):
    user_id: int
    document_name: str
    message: str


class GenerateDocumentResponseSchema(BaseModel):
    current_url: str
    previous_url: str | None = Field(default=None)

    @classmethod
    def from_entity(cls, versions: tuple[Version, Version]) -> 'GenerateDocumentResponseSchema':
        return cls(current_url=versions[0].version, previous_url=versions[1].version if versions[1] else None)


class NewVersionRequestSchema(BaseModel):
    user_id: int
    document_name: str
