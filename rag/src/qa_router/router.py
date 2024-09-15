import logging

import openai
from fastapi import APIRouter, HTTPException
from starlette import status

from qa_router.utils import generate_answer
from qa_router.schemas import Answer, Input

router = APIRouter(tags=["QA"])


@router.post("/answer", status_code=status.HTTP_200_OK, response_model=Answer)
async def answer(input: Input):
    logging.info(f"Input: {input}")

    try:
        return await generate_answer(input)
    except openai.APIStatusError as e:
        raise HTTPException(status_code=e.status_code, detail=e.response.text)