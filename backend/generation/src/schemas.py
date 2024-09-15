from pydantic import BaseModel, Field


class GenerationRequest(BaseModel):
    document_name: str
    query: str = Field(description="User's query")


class EditRequest(BaseModel):
    document_name: str
    span: str
    query: str = Field(description="User's query")


class EditResponse(BaseModel):
    html: str
