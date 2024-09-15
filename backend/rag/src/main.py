from fastapi import FastAPI
import uvicorn
from rag.qa_router.router import router as qa_router

app = FastAPI()
app.include_router(qa_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
