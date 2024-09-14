from pydantic import BaseModel


class Resolution(BaseModel):
    status: bool
    message: str
