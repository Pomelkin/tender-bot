import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from generation.src.creator.create import create
from generation.src.schemas import GenerationRequest

app = FastAPI()


@app.post("/create")
async def create_route(generation_request: GenerationRequest) -> Response:
    html_file = await create(generation_request.document_name, generation_request.query)
    
    return Response(
        content=html_file.getvalue(), 
        media_type="text/html", 
        headers={"Content-Disposition": f"attachment; filename={generation_request.document_name.split('.')[0] + '.html'}"}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
