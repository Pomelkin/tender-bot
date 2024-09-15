import os
from pyhtml2pdf import converter


def create_pdf(url: str):
    converter.convert(url, 'sample.pdf')
