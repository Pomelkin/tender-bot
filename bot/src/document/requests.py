import logging
from contextlib import asynccontextmanager

import aiohttp
from aiohttp import ClientResponse
from fastapi import HTTPException

from config import settings


@asynccontextmanager
async def send(url: str, method: str, headers: dict, proxy: str, data: dict | bytes = None) -> ClientResponse:
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        if isinstance(data, bytes):
            request_params = {"data": data}
        else:
            request_params = {"json": data}

        async with session.request(method, url, headers=headers, proxy=proxy, **request_params) as resp:
            if resp.ok:
                yield resp
            else:
                error_text = await resp.text()
                logging.error(f"Error: {error_text}")
                raise HTTPException(status_code=resp.status, detail=error_text)


async def send_check_documents(data: dict) -> dict:
    async with send(f"{settings.base_url}/...", "POST", data) as resp:
        return await resp.json()
