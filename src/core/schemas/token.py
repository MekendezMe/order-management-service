from pydantic import BaseModel

from core.schemas.user import UserRead


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserRead

class TokenData(BaseModel):
    user_id: int | None = None