from fastapi import APIRouter, Depends, status, Body, HTTPException

from core.config import settings
from core.dependencies.services import get_user_service
from core.schemas.user import UserRead, UserCreate, UserLogin
from core.services.user_service import UserService

router = APIRouter(
    tags=["Users"]
)

@router.post("/register", response_model=UserRead, status_code=status.HTTP_200_OK)
async def register(
        user_create: UserCreate = Body(..., description="Данные для регистрации"),
        user_service: UserService = Depends(get_user_service)
) -> UserRead:
    try:
        return await user_service.register(user_create)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=UserRead, status_code=status.HTTP_200_OK)
async def login(
        user_login: UserLogin = Body(..., description="Данные для авторизации"),
        user_service: UserService = Depends(get_user_service)
) -> UserRead:
    try:
        return await user_service.login(user_login)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
