from domain.entities.document import Document
from domain.entities.version import Version


def convert_version_mongo_to_entity(version: dict):
    return Version(id=version['id'], parent_document_name=version['parent_document_name'], version=version['version'])


def convert_document_mongo_to_entity(document: dict):
    return
