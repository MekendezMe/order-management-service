import decimal

from pydantic import BaseModel

from core.schemas.product import ProductRead
from core.schemas.user import UserRead


class BasketRead(BaseModel):
    id: int
    product: ProductRead
    user: UserRead
    count: int

class BasketCreate(BaseModel):
    product_id: int
    user_id: int
    count: int

class BasketItem(BaseModel):
    user_id: int
    product_id: int

class BasketItemWithoutUser(BaseModel):
    id: int
    product: ProductRead
    count: int

class BasketTotal(BaseModel):
    count: int
    price: decimal.Decimal
    discount_price: decimal.Decimal
    total_saved: decimal.Decimal

class BasketForUserResponse(BaseModel):
    user: UserRead
    items: list[BasketItemWithoutUser]
    total: BasketTotal

