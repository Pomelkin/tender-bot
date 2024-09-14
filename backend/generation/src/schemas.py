from pydantic import BaseModel, Field


class GenerationRequest(BaseModel):
    document_name: str
    query: str = Field(description="User's query")
    