from fastapi import APIRouter, Depends, status, Body, Path, HTTPException

from core.dependencies.auth import get_current_user
from core.dependencies.services import get_basket_service
from core.schemas.basket import BasketRead, BasketCreate, BasketItem, BasketForUserResponse
from core.services.basket_service import BasketService

router = APIRouter(
    tags=["Baskets"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=BasketRead, status_code=status.HTTP_201_CREATED)
async def create(
        basket_create: BasketCreate = Body(..., description="Данные для добавления товара в корзину"),
        basket_service: BasketService = Depends(get_basket_service),
) -> BasketRead:
    try:
        return await basket_service.add(basket_create)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{id}", response_model=BasketRead, status_code=status.HTTP_200_OK)
async def update(
        id: int = Path(ge=1, description="ID товара в корзине"),
        count: int = Body(..., description="Новое количество товара"),
        basket_service: BasketService = Depends(get_basket_service),
) -> BasketRead:
    try:
        return await basket_service.update(id, count)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/get/{user_id}", response_model=BasketForUserResponse, status_code=status.HTTP_200_OK)
async def get(
        user_id: int = Path(ge=1, description="ID пользователя"),
        basket_service: BasketService = Depends(get_basket_service),
) -> BasketForUserResponse:
    try:
        return await basket_service.get_user_items(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id}", response_model=bool, status_code=status.HTTP_200_OK)
async def delete(
        id: int = Path(ge=1, description="Данные для удаления товара из корзины"),
        basket_service: BasketService = Depends(get_basket_service),
) -> bool:
    try:
        return await basket_service.delete(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/removeItem", response_model=bool, status_code=status.HTTP_200_OK)
async def remove_item_from_basket(
        basket_item: BasketItem = Body(..., description="Данные для удаления конкретного товара из корзины"),
        basket_service: BasketService = Depends(get_basket_service),
) -> bool:
    try:
        return await basket_service.delete_basket_item(basket_item)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/removeAllItems/{user_id}", response_model=bool, status_code=status.HTTP_200_OK)
async def remove_all_items_from_basket(
        user_id: int = Path(ge=1),
        basket_service: BasketService = Depends(get_basket_service),
) -> bool:
    try:
        return await basket_service.delete_all_items(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )