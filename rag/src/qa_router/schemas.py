from enum import Enum
from typing import List, Optional, Union, Dict, NamedTuple
from uuid import UUID

from pydantic import BaseModel, Field, validator, field_validator


class Role(str, Enum):
    USER = "user"
    AI = "ai"


class Message(BaseModel):
    role: Role
    content: str


class Input(BaseModel):
    vault_id: str = Field(examples=["текст.txt"])
    query: str = Field(description="User's new message")


# class SearchResult(BaseModel):
#     document_id: UUID
#     document_name: str
#     information: str


class SearchResult(NamedTuple):
    page_content: str


class Answer(BaseModel):
    content: str



