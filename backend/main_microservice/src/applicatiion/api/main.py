from fastapi import FastAPI
import uvicorn

from applicatiion.api.handlers import router as documents


def create_app():
    app = FastAPI(
        title="DataChad",
        description="DataChad API app",
        version="0.0.1",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        debug=True,
    )
    app.include_router(documents)
    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="10.14.156.23", port=8000)