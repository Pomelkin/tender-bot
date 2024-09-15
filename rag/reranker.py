import aiohttp

from rag.config import settings


class Reranker:
    """
    Reranker interface for reranking data from the knowledge base.
    """

    def __init__(self):
        self.url = (
            f"http://{settings.reranker.host}:{settings.reranker.port}/v1/reranker"
        )

    async def rerank(self, query: str, documents: list[str]) -> list[str]:
        """
        Rerank documents based on the query.

        :param query: Query to rerank documents.
        :param documents: List of documents to rerank.
        :return: List of reranked documents
        """

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url, json={"query": query, "documents": documents}
            ) as response:
                results = await response.json()
                return results["documents"]
