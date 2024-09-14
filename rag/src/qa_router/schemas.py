from enum import Enum
from typing import List, Optional, Union, Dict
from uuid import UUID

from pydantic import BaseModel, Field, validator, field_validator


class Role(str, Enum):
    USER = "user"
    AI = "ai"


class Message(BaseModel):
    role: Role
    content: str


class Input(BaseModel):
    vault_id: str = Field(examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"])
    query: str = Field(description="User's new message")
    history: List[Dict[str, str]] = Field(examples=[[{"role": "user", "content": "Hello"}]], description="Chat history")

    @validator('history', pre=True, each_item=True)
    def clean_history(cls, value):
        if 'role' in value and value['role'] == 'ai':
            value['role'] = 'assistant'
        value = {k: v for k, v in value.items() if k in {'content', 'role'}}
        return value


class SearchResult(BaseModel):
    document_id: UUID
    document_name: str
    information: str


class Answer(BaseModel):
    content: str
    traceback: List[SearchResult]
