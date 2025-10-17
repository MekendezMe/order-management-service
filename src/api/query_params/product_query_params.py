import decimal
from typing import Optional
from fastapi import Query

from core.repositories.helpers.pagination_params import PaginationParams
from core.repositories.helpers.sort_params import SortParams
from core.schemas.product_filters import ProductFilter


class ProductQueryParams:
    def __init__(
            self,
            min_price: Optional[decimal.Decimal] = Query(None, ge=0, description="Минимальная цена"),
            max_price: Optional[decimal.Decimal] = Query(None, ge=0, description="Максимальная цена"),
            min_age: Optional[int] = Query(None, ge=0, le=100, description="Минимальный возраст"),
            in_stock_only: bool = Query(False, description="Количество на складе"),
            author_id: Optional[int] = Query(None, description="Автор"),

            sort_by: str = Query("id", description="Сортировка по полю"),
            sort_order: str = Query("desc", description="Направление сортировки"),

            page: int = Query(1, ge=1, description="Номер страницы"),
            limit: int = Query(50, ge=1, le=100, description="Количество записей")
    ):
        self.product_filter = ProductFilter(
            min_price=min_price,
            max_price=max_price,
            min_age=min_age,
            in_stock_only=in_stock_only,
            author_id=author_id
        )

        self.sort_params = SortParams(
            sort_by=sort_by,
            sort_order=sort_order
        )

        self.pagination_params = PaginationParams(
            limit=limit,
            offset=(page - 1) * limit
        )