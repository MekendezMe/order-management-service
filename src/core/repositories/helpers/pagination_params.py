from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    limit: int = Field(10, le=100, ge=0)
    offset: int = Field(0, ge=0)
