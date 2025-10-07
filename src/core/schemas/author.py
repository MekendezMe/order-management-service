from pydantic import BaseModel


class AuthorRead(BaseModel):
    id: int
    name: str
    verified: bool