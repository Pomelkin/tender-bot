import logging
from typing import List
from openai import AsyncClient
from rag.reranker import Reranker
from rag.qa_router.prompts import USER_PROMPT_QA, SYSTEM_PROMPT_QA
from rag.qa_router.schemas import Input
from rag.vector_db.queries import search_relevant_chunks
from rag.config import settings
from rag.qa_router.schemas import Answer

embeddings_url = f"http://{settings.embeddings.host}:{settings.embeddings.port}/v1/"
llm_url = f"http://{settings.gemma2.host}:{settings.gemma2.port}/v1"
reranker = Reranker()
openai_client = AsyncClient(base_url=embeddings_url, api_key="password")


async def generate_answer(input: Input):
    logging.info("Using documents db")
    embedding = await create_embedding(input.query)

    result_from_doc = await search_relevant_chunks(
        vault_id=input.vault_id, vector=embedding, top_k=5
    )
    result_from_fz = await search_relevant_chunks(
        vault_id=settings.qdrant.fz44, vector=embedding, top_k=5
    )

    doc_payloads = [x.page_content for x in result_from_doc]
    fz_payloads = [x.page_content for x in result_from_fz]

    ranked_doc_payloads = await reranker.rerank(
        query=input.query, documents=doc_payloads
    )
    ranked_fz_payloads = await reranker.rerank(
        query=input.query,
        documents=fz_payloads,
    )

    ranked_result = ranked_doc_payloads + ranked_fz_payloads

    text = "\n\n".join(ranked_result)
    print(text)

    answer = await create_completion_with_context(query=input.query, context=text)
    return Answer(content=answer)


async def create_embedding(query: str) -> List[float]:
    openai_client.base_url = embeddings_url
    response = await openai_client.embeddings.create(input=[query], model=" ")
    return list(map(lambda x: x.embedding, response.data))[0]


async def create_completion_with_context(context: str, query: str) -> str:
    messages = [
        {
            "role": "user",
            "content": SYSTEM_PROMPT_QA
            + USER_PROMPT_QA.format(query=query, context=context),
        }
    ]
    logging.info(f"Messages: {messages}")
    answer = await create_base_completion(messages)
    return answer


async def create_base_completion(messages: list) -> str:
    openai_client.base_url = llm_url
    response = await openai_client.chat.completions.create(
        model="google/gemma-2-9b-it",
        messages=messages,
        temperature=0.0,
        max_tokens=1024,
        timeout=60 * 5,
    )
    answer = response.choices[0].message.content
    return answer
