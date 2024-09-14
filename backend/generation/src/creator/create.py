from io import BytesIO

from generation.src.creator.generate import Generator
from generation.src.utils.readers import DocumentReader
from generation.src.utils.s3 import S3Repository


async def create(document_name: str, query: str) -> BytesIO:
    s3_repository = S3Repository()

    file = await s3_repository.get(document_name)
    file_type = document_name.split(".")[-1]

    reader = DocumentReader()
    text = await reader.read(file_type, file)

    generator = Generator(max_tokens=1024)
    html_str = await generator.generate(text, query)
    file = BytesIO()
    file.write(html_str.encode("utf-8"))
    file.seek(0)
    return file
