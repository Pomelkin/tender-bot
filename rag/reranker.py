from rag.config import settings
import aiohttp


class Reranker:
    """
    Reranker interface for reranking data from the knowledge base.
    """

    def __init__(self):
        self.url = f"http://{settings.host}:{settings.port}/v1/reranker"
        self.aiohttp_session = aiohttp.ClientSession()

    async def rerank(self, query: str, documents: list[str]) -> list[str]:
        """
        Rerank documents based on the query.

        :param query: Query to rerank documents.
        :param documents: List of documents to rerank.
        :return: List of reranked documents
        """
        async with self.aiohttp_session as session:
            async with session.post(
                self.url, json={"query": query, "documents": documents}
            ) as response:
                results = await response.json()
                return results["documents"]
