from fastapi import FastAPI
import uvicorn
from rag.qa_router.router import router as qa_router

app = FastAPI()
app.include_router(qa_router)

uvicorn.run(app)
