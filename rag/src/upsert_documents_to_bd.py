import logging
import time
import uuid
from typing import List

from rag.src.vector_db.core import qdrant_instance
from rag.src.vector_db.queries import create_collection, upsert_document


async def create_knowledge_base(file_path: str) -> None:

    if await qdrant_instance.collection_exists(file_path):
        raise ValueError("Knowledge base already exists")

    relations = await request_relation_extraction(documents)

    await fill_new_kb(vault_id, relations)


async def create_embeddings(texts: List[str] | str) -> List[List[float]]:
    texts = list(map(lambda x: x.replace("\n", " "), texts))
    response = await settings.openai_client.embeddings.create(input=texts, model=" ")
    vectors = list(map(lambda x: x.embedding, response.data))
    return vectors


async def fill_new_kb(vault_id: UUID, prepared_docs: PreparedToUpsertDocuments) -> None:
    await create_collection(vault_id)
    await upsert_document(vault_id, prepared_docs)


async def request_relation_extraction(file_path: str) -> PreparedToUpsertDocuments:
    start_time = time.perf_counter()

    # splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    # docs = (splitter.create_documents([document.text],
    #                                   metadatas=[{"document_id": document.document_id,
    #                                               "document_name": document.document_name}]) for document in documents)
    #
    # flat_docs_list = [item for sublist in docs for item in sublist]

    prepared_docs = {"ids": [], 'payloads': [], 'vectors': []}

    result = await create_embeddings(list(map(lambda x: x.page_content, flat_docs_list)))

    for num, doc in enumerate(flat_docs_list):
        prepared_docs['payloads'].append(
            {'page_content': doc.page_content})
        prepared_docs["ids"].append(str(uuid.uuid4()))
        prepared_docs['vectors'].append(result[num])

    logging.info(
        f"Extracted relations from {len(documents)} documents in {time.perf_counter() - start_time:.4f} seconds"
    )

    return PreparedToUpsertDocuments(**prepared_docs)