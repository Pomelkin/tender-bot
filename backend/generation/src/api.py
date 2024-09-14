import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from generation.src.generator.create import create
from generation.src.schemas import GenerationRequest

app = FastAPI()


@app.post("/create")
async def create_route(generation_request: GenerationRequest) -> FileResponse:
    html_file = create(generation_request.document_name, generation_request.query)

    return FileResponse(
        html_file, filename=generation_request.document_name, media_type="text/html"
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
