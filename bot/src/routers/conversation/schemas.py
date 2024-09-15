from pydantic import BaseModel


class Resolution(BaseModel):
    status: bool = True
    message: str


class ShowDiff(BaseModel):
    current_url: str
    previous_url: str | None
