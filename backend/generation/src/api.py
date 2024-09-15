import uvicorn
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from generation.src.creator.create import create
from generation.src.editor.edit import edit
from generation.src.schemas import EditRequest, EditResponse, GenerationRequest

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create")
async def create_route(generation_request: GenerationRequest) -> Response:
    html_file = await create(generation_request.document_name, generation_request.query)

    return Response(
        content=html_file.getvalue(),
        media_type="text/html",
        headers={
            "Content-Disposition": f"attachment; filename={generation_request.document_name.split('.')[0] + '.html'}"
        },
    )


@app.post("/edit")
async def edit_route(edit_request: EditRequest) -> EditResponse:
    print(edit_request)
    html_str = await edit(
        edit_request.document_name, edit_request.span, edit_request.query
    )
    return EditResponse(html=html_str)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
