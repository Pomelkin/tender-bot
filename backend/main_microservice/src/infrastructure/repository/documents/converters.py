from domain.entities.document import Document
from domain.entities.version import Version


def convert_version_mongo_to_entity(version: dict):
    return Version(id=version['id'], parent_document_id=version['parent_document_id'], customer_id=version['customer_id'], performer_id=version['performer_id'], version_url=version['version_url'])


def convert_document_mongo_to_entity(document: dict):
    return