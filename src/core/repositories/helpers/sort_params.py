from pydantic import BaseModel


class SortParams(BaseModel):
    sort_by: str = "id"
    sort_order: str = "desc"