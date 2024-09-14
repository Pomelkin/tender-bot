from io import BytesIO

from generation.src.generator.generate import generate
from generation.src.utils.readers import read_doc, read_docx, read_pdf
from generation.src.utils.s3 import S3Repository


async def create(document_name: str, query: str) -> BytesIO:
    s3_repository = S3Repository()

    file = await s3_repository.get(document_name)
    file_type = document_name.split(".")[-1]

    if file_type == "pdf":
        text = await read_doc(file)
    elif file_type == "docx":
        text = await read_docx(file)
    else:
        text = await read_pdf(file)

    html_str = await generate(text, query)
    file = BytesIO()
    file.write(html_str.encode("utf-8"))
    file.seek(0)
    return file
