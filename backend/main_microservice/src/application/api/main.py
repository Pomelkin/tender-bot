from fastapi import FastAPI
import uvicorn

from application.api.handlers import router as documents


def create_app():
    app = FastAPI(
        title="Tender-bot",
        description="Tender API",
        version="0.0.1",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        debug=True,
    )
    app.include_router(documents)
    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)