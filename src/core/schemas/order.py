import decimal

from pydantic import BaseModel

from core.schemas.order_product import OrderProductWithoutOrderId
from core.schemas.status import StatusRead
from core.schemas.user import UserRead


class OrderRead(BaseModel):
    id: int
    user: UserRead
    count: int
    price: decimal.Decimal
    status: StatusRead


class OrderItemCreate(BaseModel):
    product_id: int
    count: int
    price: decimal.Decimal

class OrderCreate(BaseModel):
    user_id: int
    items: list[OrderItemCreate]

class OrderWithProducts(OrderRead):
    products: list[OrderProductWithoutOrderId]


