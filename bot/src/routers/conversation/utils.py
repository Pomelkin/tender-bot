import os
from pyhtml2pdf import converter


def create_pdf():
    path = os.path.abspath('sample.html')
    converter.convert(f'file:///{path}', 'sample.pdf')