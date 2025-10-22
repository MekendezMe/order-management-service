import decimal

from pydantic import BaseModel

from core.schemas.order import OrderRead
from core.schemas.product import ProductRead


class OrderProductRead(BaseModel):
    id: int
    order: OrderRead
    product: ProductRead
    count: int
    price: decimal.Decimal
