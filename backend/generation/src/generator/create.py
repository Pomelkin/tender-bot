from io import BytesIO

from generation.src.generator.generate import generate
from generation.src.utils.readers import read_doc, read_docx, read_pdf
from generation.src.utils.s3 import S3Repository


def create(document_name: str, query: str) -> BytesIO:
    s3_repository = S3Repository()

    file = s3_repository.get(document_name)
    file_type = document_name.split(".")[-1]

    if file_type == "pdf":
        text = read_doc(file)
    elif file_type == "docx":
        text = read_docx(file)
    else:
        text = read_pdf(file)

    html_str = generate(text, query)
    file = BytesIO()
    file.write(html_str.encode("utf-8"))
    file.seek(0)
    return file
