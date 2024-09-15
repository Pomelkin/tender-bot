import logging
from typing import List

from openai import AsyncClient

from rag.qa_router.prompts import USER_PROMPT_QA, SYSTEM_PROMPT_QA
from rag.qa_router.schemas import Input
from rag.vector_db.queries import search_relevant_chunks

from rag.qa_router.schemas import Answer

embeddings_url = "http://pomelk1n-dev.su:8005/v1/"
llm_url = "http://pomelk1n-dev.su:8000/v1"

openai_client = AsyncClient(base_url="http://example.com", api_key="password")


async def generate_answer(input: Input):
    logging.info("Using documents db")
    embedding = await create_embedding(input.query)
    result = await search_relevant_chunks(
        vault_id=input.vault_id, vector=embedding, top_k=4
    )
    # тут реранк
    text = "\n\n".join([x.page_content for x in result])
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
