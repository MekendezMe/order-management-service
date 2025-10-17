from pydantic import BaseModel

class RoleRead(BaseModel):
    id: int
    name: str