from uuid import UUID

from rag.qa_router.schemas import SearchResult
from rag.vector_db.core import qdrant_instance
from qdrant_client.http.models import models, VectorParams

from rag.src.schemas import PreparedToUpsertDocuments


async def upsert_document(file_name: str, prepared_docs: PreparedToUpsertDocuments):
    await qdrant_instance.upsert(
        file_name, points=models.Batch(**prepared_docs.model_dump(mode="json"))
    )


async def create_collection(file_name: str):
    await qdrant_instance.create_collection(
        file_name,
        vectors_config=VectorParams(size=1024, distance=models.Distance.COSINE),
    )


async def drop_database(vault_id: UUID):
    await qdrant_instance.delete_collection(vault_id)


async def drop_document(vault_id: UUID, document_id: UUID):
    qdrant_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="document_id",
                match=models.MatchValue(value=str(document_id)),
            )
        ]
    )

    await qdrant_instance.delete(vault_id, qdrant_filter)


async def search_relevant_chunks(
    vault_id: str, vector: list[float], top_k: int
) -> list[SearchResult]:
    response = await qdrant_instance.search(
        collection_name=vault_id, query_vector=vector, limit=top_k
    )
    search_result = [
        SearchResult(page_content=x.payload["page_content"]) for x in response
    ]
    return search_result
