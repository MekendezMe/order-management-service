import decimal
from typing import Optional, List

from pydantic import BaseModel


class ProductFilter(BaseModel):
    min_price: Optional[decimal.Decimal] = None,
    max_price: Optional[decimal.Decimal] = None,
    min_age: Optional[int] = None,
    in_stock_only: Optional[bool] = False,
    author_id: Optional[int] = None