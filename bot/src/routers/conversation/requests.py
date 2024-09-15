import logging
from contextlib import asynccontextmanager

import aiohttp
from aiohttp import ClientResponse
from fastapi import HTTPException

from config import settings


@asynccontextmanager
async def send(url: str, method: str, data: dict | bytes = None) -> ClientResponse:
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        if isinstance(data, bytes):
            request_params = {"data": data}
        else:
            request_params = {"json": data}

        async with session.request(method, url, **request_params) as resp:
            if resp.ok:
                yield resp
            else:
                error_text = await resp.text()
                logging.error(f"Error: {error_text}")
                raise HTTPException(status_code=resp.status, detail=error_text)


async def send_user_query(data: dict) -> dict:
    async with send(f"{settings.BASE_URL_RAG}/answer", "POST", data) as resp:
        return await resp.json()


async def send_create_agreement(data: dict) -> dict:
    logging.info(f"{settings.BASE_URL_GENERATE}/generate-document")
    async with send(f"{settings.BASE_URL_GENERATE}/generate-document", "POST", data) as resp:
        return await resp.json()


async def delete_old_versions(data: dict) -> tuple[int, dict]:
    async with send(f"{settings.BASE_URL_GENERATE}/delete-versions", "DELETE", data) as resp:
        return resp.status, await resp.json()