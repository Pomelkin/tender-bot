from pydantic import BaseModel


class RerankerRequest(BaseModel):
    query: str
    documents: list[str]
