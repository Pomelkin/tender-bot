from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, File, Response
from punq import Container

from application.api.schemas import GenerateDocumentRequestSchema, GenerateDocumentResponseSchema, ErrorSchema, \
    NewVersionRequestSchema
from domain.exceptions.base import ApplicationException
from logic.commands.documents import GenerateDocument, UploadNewVersion
from logic.mediator import Mediator
from logic import init_container

router = APIRouter(tags=["Documents"])


@router.post("/generate-document",
             status_code=status.HTTP_201_CREATED,
             description="Эндпоинт для генерации нового доп соглашения",
             responses={
                 status.HTTP_201_CREATED: {"model": GenerateDocumentResponseSchema},
                 status.HTTP_406_NOT_ACCEPTABLE: {"model": ErrorSchema},
                 status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorSchema},
             })
async def generate_document(document: GenerateDocumentRequestSchema, container: Container = Depends(init_container)):
    try:
        mediator: Mediator = container.resolve(Mediator)
        versions, *_ = await mediator.handle_command(GenerateDocument(document_name=document.document_name, message=document.message, user_id=document.user_id))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"error": e.message})
    except Exception as e:
        raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'error': "Непредвиденная ошибка"})
    return GenerateDocumentResponseSchema.from_entity(versions)


@router.post("/new-version",
             status_code=status.HTTP_202_ACCEPTED,
             description="Обновляет последнюю версию с фронта",
             responses={
                 status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
                 status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorSchema},
             })
async def new_version(version_file: Annotated[str, File(..., media_type="text/html")], version: NewVersionRequestSchema=Depends(), container: Container = Depends(init_container)):
    try:
        mediator: Mediator = container.resolve(Mediator)
        await mediator.handle_command(UploadNewVersion(user_id=version.user_id, document_name=version.document_name, version_file=version_file.encode("utf-8")))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": e.message})
    except Exception as e:
        raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": "Непредвиденная ошибка"})
    return status.HTTP_202_ACCEPTED
