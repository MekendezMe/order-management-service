import decimal

from pydantic import BaseModel

class ProductQuantity(BaseModel):
    product_id: int
    quantity: int

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

class ProductBase(BaseModel):
    name: str
    description: str
    price: decimal.Decimal
    discount_price: decimal.Decimal
    stock_quantity: int
    image: str
    minimal_age: int

class ProductCreate(ProductBase):
    author: str

class ProductUpdate(ProductBase):
    id: int
    article: str