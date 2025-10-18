import decimal

from pydantic import BaseModel

from core.schemas.author import AuthorRead


class ProductQuantity(BaseModel):
    product_id: int
    quantity: int

class ProductRead(BaseModel):
    id: int
    article: str
    name: str
    description: str
    author: AuthorRead
    price: decimal.Decimal
    discount_price: decimal.Decimal
    stock_quantity: int
    image: str
    minimal_age: int
    is_active: bool

class ProductBase(BaseModel):
    name: str
    description: str
    price: decimal.Decimal
    discount_price: decimal.Decimal
    stock_quantity: int
    image: str
    minimal_age: int

class ProductCreate(ProductBase):
    author_id: int

class ProductUpdate(ProductBase):
    ...