async def create_knowledge_base(input: DocumentsInput) -> None:
    vault_id = input.vault_id
    documents = input.documents

    if await qdrant_store.collection_exists(vault_id):
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


async def request_relation_extraction(
        documents: List[Document],
) -> PreparedToUpsertDocuments:
    start_time = time.perf_counter()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = (splitter.create_documents([document.text],
                                      metadatas=[{"document_id": document.document_id,
                                                  "document_name": document.document_name}]) for document in documents)

    flat_docs_list = [item for sublist in docs for item in sublist]
    prepared_docs = {"ids": [], 'payloads': [], 'vectors': []}

    result = await create_embeddings(list(map(lambda x: x.page_content, flat_docs_list)))

    for num, doc in enumerate(flat_docs_list):
        prepared_docs['payloads'].append(
            {'page_content': doc.page_content, **doc.metadata})
        prepared_docs["ids"].append(str(uuid.uuid4()))
        prepared_docs['vectors'].append(result[num])

    logging.info(
        f"Extracted relations from {len(documents)} documents in {time.perf_counter() - start_time:.4f} seconds"
    )

    return PreparedToUpsertDocuments(**prepared_docs)