import decimal

from pydantic import BaseModel

from core.schemas.product import ProductRead
from core.schemas.user import UserRead


class BasketRead(BaseModel):
    id: int
    product: ProductRead
    user: UserRead
    count: int
    price: decimal.Decimal
