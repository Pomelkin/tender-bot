import logging
from io import BytesIO

from fastapi import HTTPException
from generation.src.creator.generate import Generator
from generation.src.creator.prompts import validation_query_prompt
from generation.src.creator.requests import request_rag
from generation.src.utils.readers import DocumentReader
from generation.src.utils.s3 import S3Repository


async def create(document_name: str, query: str) -> BytesIO:
    s3_repository = S3Repository()

    file = await s3_repository.get(document_name)
    file_type = document_name.split(".")[-1]

    reader = DocumentReader()
    text = await reader.read(file_type, file)

    validation_query = validation_query_prompt.format(query)
    validation = await request_rag(document_name, validation_query)
    logging.info(validation)

    generator = Generator()
    
    verdict = await generator.generate_verdict(validation)

    if verdict:
        html_str = await generator.generate(text, query)
        file = BytesIO()
        file.write(html_str.encode("utf-8"))
        file.seek(0)
        return file
    else:
        raise HTTPException(status_code=406, detail=validation)
