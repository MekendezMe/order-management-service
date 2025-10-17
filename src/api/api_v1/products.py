from fastapi import APIRouter, status, Body, Depends, HTTPException

from api.query_params.product_query_params import ProductQueryParams
from core.dependencies.services import get_product_service
from core.schemas.product import ProductRead, ProductCreate, ProductUpdate
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

@router.post("/update", response_model=ProductRead, status_code=status.HTTP_200_OK)
async def update(
        product_update: ProductUpdate = Body(..., description="Данные для обновления продукта"),
        product_service: ProductService = Depends(get_product_service)
) -> ProductRead:
    try:
        return await product_service.update(product_update)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/select", response_model=list[ProductRead], status_code=status.HTTP_200_OK)
async def get(
        params: ProductQueryParams = Depends(),
        product_service: ProductService = Depends(get_product_service)
) -> list[ProductRead]:
    try:
        return await product_service.get(params)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )