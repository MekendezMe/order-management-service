import decimal

from pydantic import BaseModel

from core.schemas.product import ProductRead
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

class OrderCreate(BaseModel):
    user_id: int
    items: list[OrderItemCreate]

class OrderProductWithoutOrderId(BaseModel):
    id: int
    product: ProductRead
    count: int
    price: decimal.Decimal

class OrderWithProducts(BaseModel):
    order: OrderRead
    products: list[OrderProductWithoutOrderId]


