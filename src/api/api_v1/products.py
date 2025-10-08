from fastapi import APIRouter, status, Body, Depends, HTTPException

from core.dependencies.services import get_product_service
from core.schemas.product import ProductRead, ProductCreate
from core.services.product_service import ProductService

router = APIRouter(
    tags=["Products"]
)

@router.post("/create", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def register(
        product_create: ProductCreate = Body(..., description="Данные для создания продукта"),
        product_service: ProductService = Depends(get_product_service)
) -> ProductRead:
    try:
        return await product_service.create(product_create)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )