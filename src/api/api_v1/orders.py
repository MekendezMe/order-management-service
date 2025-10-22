from fastapi import APIRouter, Depends, status, HTTPException, Path, Body, Query

from core.dependencies.auth import get_current_user
from core.dependencies.services import get_order_service
from core.schemas.order import OrderRead, OrderCreate, OrderWithProducts
from core.services.order_service import OrderService

router = APIRouter(
    tags=["Orders"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=OrderWithProducts, status_code=status.HTTP_201_CREATED)
async def create(
        order_create: OrderCreate = Body(..., description="Данные для создания заказа"),
        order_service: OrderService = Depends(get_order_service),
) -> OrderWithProducts:
    try:
        return await order_service.create(order_create)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{id}", response_model=OrderRead, status_code=status.HTTP_200_OK)
async def update(
        id: int = Path(ge=1, description="ID заказа"),
        status_id: int = Body(..., description="Новый статус"),
        order_service: OrderService = Depends(get_order_service),
) -> OrderRead:
    try:
        return await order_service.update(id, status_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/get/{order_id}", response_model=OrderWithProducts, status_code=status.HTTP_200_OK)
async def get(
        order_id: int = Path(ge=1, description="ID заказа"),
        order_service: OrderService = Depends(get_order_service),
) -> OrderWithProducts:
    try:
        return await order_service.get_one(order_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/getAll/{user_id}", response_model=list[OrderWithProducts], status_code=status.HTTP_200_OK)
async def get(
        user_id: int = Path(ge=1, description="ID пользователя"),
        order_service: OrderService = Depends(get_order_service),
) -> list[OrderWithProducts]:
    try:
        return await order_service.get_all_by_user(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id}", response_model=bool, status_code=status.HTTP_200_OK)
async def delete(
        id: int = Path(ge=1, description="Данные для удаления заказа"),
        order_service: OrderService = Depends(get_order_service),
) -> bool:
    try:
        return await order_service.delete(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )