from fastapi import APIRouter

from core.config import settings
from .users import router as users_router
from .products import router as products_router
from .baskets import router as baskets_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)

router.include_router(users_router, prefix=settings.api.v1.users)
router.include_router(products_router, prefix=settings.api.v1.products)
router.include_router(baskets_router, prefix=settings.api.v1.baskets)
