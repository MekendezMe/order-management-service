from fastapi import APIRouter, status, Body, Depends, HTTPException, Query, Path

from api.query_params.product_query_params import ProductQueryParams
from core.dependencies.auth import get_current_user
from core.dependencies.services import get_product_service
from core.schemas.product import ProductRead, ProductCreate, ProductUpdate
from core.services.product_service import ProductService

router = APIRouter(
    tags=["Products"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create(
        product_create: ProductCreate = Body(..., description="Данные для создания продукта"),
        product_service: ProductService = Depends(get_product_service),
) -> ProductRead:
    try:
        return await product_service.create(product_create)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
async def update(
        id: int = Path(ge=1, description="ID продукта"),
        product_update: ProductUpdate = Body(..., description="Данные для обновления продукта"),
        product_service: ProductService = Depends(get_product_service),
) -> ProductRead:
    try:
        return await product_service.update(id, product_update)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/get", response_model=list[ProductRead], status_code=status.HTTP_200_OK)
async def get(
        params: ProductQueryParams = Depends(),
        product_service: ProductService = Depends(get_product_service),
) -> list[ProductRead]:
    try:
        return await product_service.get(params)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id}", response_model=bool, status_code=status.HTTP_200_OK)
async def delete(
        id: int = Path(ge=1, description="Данные для удаления продукта"),
        product_service: ProductService = Depends(get_product_service),
) -> bool:
    try:
        return await product_service.delete(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )