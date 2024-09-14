import logging
import re
import time
import uuid
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.src.vector_db.core import qdrant_instance
from rag.src.vector_db.queries import create_collection, upsert_document
from schemas import PreparedToUpsertDocuments


async def create_knowledge_base(file_path: str) -> None:
    if await qdrant_instance.collection_exists(file_path):
        raise ValueError("Knowledge base already exists")

    docs = await process_document(file_path)

    await fill_new_kb(file_path, docs)


async def create_embeddings(texts: List[str] | str) -> List[List[float]]:
    texts = list(map(lambda x: x.replace("\n", " "), texts))
    response = await settings.openai_client.embeddings.create(input=texts, model=" ")
    vectors = list(map(lambda x: x.embedding, response.data))
    return vectors


async def fill_new_kb(file_name: str, prepared_docs: PreparedToUpsertDocuments) -> None:
    await create_collection(file_name)
    await upsert_document(file_name, prepared_docs)


def parse_contract(text):
    pattern = r'(^\d+\.\d+)\.\s*((?:(?!^\d+\.\d+\.).|\n)+)'

    # Поиск совпадений
    matches = re.findall(pattern, text, re.MULTILINE)

    if matches:
        result = []
        for match in matches:
            # result[match[0]] = match[1].strip()  # Убираем лишние пробелы
            result.append((match[0] + '\n' + match[1]))
        return result
    else:
        return [text]


async def process_document(file_path: str) -> PreparedToUpsertDocuments:
    start_time = time.perf_counter()

    with open(file_path) as f:
        file_text = f.read()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    texts = text_splitter.create_documents([file_text])

    final = []

    for doc in texts:
        page_content = doc.page_content
        final = final + parse_contract(page_content)

    flat_docs_list = [Document(page_content=page_content) for page_content in final]

    prepared_docs = {"ids": [], 'payloads': [], 'vectors': []}

    result = await create_embeddings(list(map(lambda x: x.page_content, flat_docs_list)))

    for num, doc in enumerate(flat_docs_list):
        prepared_docs['payloads'].append(
            {'page_content': doc.page_content})
        prepared_docs["ids"].append(str(uuid.uuid4()))
        prepared_docs['vectors'].append(result[num])

    logging.info(
        f"took {time.perf_counter() - start_time:.4f} seconds"
    )

    return PreparedToUpsertDocuments(**prepared_docs)
