from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from punq import Container

from application.api.schemas import GenerateDocumentRequestSchema, GenerateDocumentResponseSchema
from domain.exceptions.base import ApplicationException
from logic.commands.documents import Consulate, GenerateDocument
from logic.mediator import Mediator
from logic import init_container

router = APIRouter(tags=["Documents"])


@router.post("/generate-document")
async def generate_document(document: GenerateDocumentRequestSchema = Depends(), container: Container = Depends(init_container)):
    try:
        mediator: Mediator = container.resolve(Mediator)
        versions, *_ = await mediator.handle_command(GenerateDocument(document_name=document.document_name, message=document.message, user_id=document.user_id))
    except ApplicationException as e:
        raise HTTPException(400)
    return GenerateDocumentResponseSchema.from_entity(versions)
