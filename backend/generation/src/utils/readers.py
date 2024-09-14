from io import BytesIO

import docx
from PyPDF2 import PdfReader
#from spire.doc import Document as SpireDocument


def read_pdf(bytesio_obj: BytesIO):
    """
    Reads a PDF from a BytesIO object and returns its text content as a string.
    """
    pdf_reader = PdfReader(bytesio_obj)
    text = ""
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    return text


def read_docx(bytesio_obj: BytesIO):
    """
    Reads a DOCX file from a BytesIO object and returns its text content as a string.
    """
    doc = docx.Document(bytesio_obj)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


def read_doc(bytesio_obj: BytesIO) -> str:
    """
    Reads a .doc file from a BytesIO object and returns its text content as a string.
    """
    '''document = SpireDocument()
    document.LoadFromStream(bytesio_obj)

    text = document.GetText()
    return text[71:]'''
    pass


if __name__ == "__main__":
    # Example usage:
    with open("example.pdf", "rb") as f:
        pdf_bytes = BytesIO(f.read())
