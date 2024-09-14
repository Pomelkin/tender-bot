from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from punq import Container
from pydantic import BaseModel

from domain.exceptions.base import ApplicationException
from logic import init_container


class ErrorSchema(BaseModel):
    error: str


class ConsultationRequestSchema(BaseModel):
    document_id: str
    message: str


class ConsultationResponseSchema(BaseModel):
    message: str


class GenerateDocumentRequestSchema(BaseModel):
    user_id: int
    document_id: str
    message: str


class GenerateDocumentResponseSchema(BaseModel):
    message: str
