from uuid import UUID
# from database.qdrant import client as qdrant_store
from core import client_qdrant
from qdrant_client.http.models import models, VectorParams

from kb_router.schemas import PreparedToUpsertDocuments


async def upsert_document(vault_id: UUID, prepared_docs: PreparedToUpsertDocuments):
    await qdrant_store.upsert(vault_id, points=models.Batch(**prepared_docs.model_dump(mode="json")))


async def create_collection(vault_id: UUID):
    await qdrant_store.create_collection(vault_id, vectors_config=VectorParams(size=384,
                                                                               distance=models.Distance.COSINE))


async def drop_database(vault_id: UUID):
    await qdrant_store.delete_collection(vault_id)


async def drop_document(vault_id: UUID, document_id: UUID):
    qdrant_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="document_id",
                match=models.MatchValue(
                    value=str(document_id)
                ),
            )
        ]
    )

    await qdrant_store.delete(vault_id, qdrant_filter)


async def search_relevant_chunks(vault_id: str, vector: list[float], top_k: int) -> RelevantChunksResult:
    response = await qdrant_store.search(collection_name=vault_id,
                                         query_vector=vector,
                                         limit=top_k)

    result_text = '\n\n'.join(list(map(lambda x: x.payload['page_content'], response)))
    logging.info(f"Result text: {result_text}")
    search_result = [SearchResult(document_id=x.payload['document_id'],
                                  information=x.payload['page_content'],
                                  document_name=x.payload.get('document_name', "no_name_found")) for x in response]
    return RelevantChunksResult(text=result_text, search_result=search_result)