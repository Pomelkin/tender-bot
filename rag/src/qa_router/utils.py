import logging
from typing import List, Any

from qa_router.prompts import USER_PROMPT_QA, SYSTEM_PROMPT_THOUGH, USER_PROMPT_THOUGH, SYSTEM_PROMPT_QA
from qa_router.schemas import Input
from config import settings
from database.queries import search_relevant_chunks

from qa_router.schemas import Answer


async def generate_answer(input: Input):
    logging.info("Using documents db")
    embedding = await create_embedding(input.query)
    result = await search_relevant_chunks(vault_id=input.vault_id, vector=embedding, top_k=4)
    answer = await create_completion_with_context(query=input.query, context=result.text,
                                                  messages_history=input.history)
    return Answer(content=answer, traceback=result.search_result)


async def create_embedding(query: str) -> List[float]:
    settings.openai_client.base_url = settings.URL_TO_EMBEDDINGS
    response = await settings.openai_client.embeddings.create(input=[query], model=" ")
    return list(map(lambda x: x.embedding, response.data))[0]


async def create_completion_with_context(context: Any, query: str, messages_history: list) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT_QA}] + \
               messages_history + \
               [{"role": "user", "content": USER_PROMPT_QA.format(query=query, context=context)}]
    logging.info(f"Messages: {messages}")
    answer = await create_base_completion(messages)
    return answer


async def create_base_completion(messages: list) -> str:
    settings.openai_client.base_url = settings.URL_TO_LLM
    response = await settings.openai_client.chat.completions.create(model="suzume-llama-3-8B-multilingual-gptq-8bit",
                                                                    messages=messages,
                                                                    temperature=0.0,
                                                                    max_tokens=1024,
                                                                    timeout=60 * 5,
                                                                    extra_body={"stop_token_ids": [128009]}, )
    answer = response.choices[0].message.content

    if "<|eot_id|>" in answer:
        answer.replace('<|eot_id|>', '')

    return answer
