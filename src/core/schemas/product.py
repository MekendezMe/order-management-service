import decimal

from pydantic import BaseModel


class ProductRead(BaseModel):
    id: int
    article: str
    name: str
    description: str
    author: str
    price: decimal.Decimal
    discount_price: decimal.Decimal
    stock_quantity: int
    image: str
    minimal_age: int
    is_active: bool

class ProductCreate(BaseModel):
    name: str
    description: str
    author: str
    price: decimal.Decimal
    discount_price: decimal.Decimal
    stock_quantity: int
    image: str
    minimal_age: int