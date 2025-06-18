from fastapi import APIRouter

from app.api.endpoints import dish, order

api_router = APIRouter()
api_router.include_router(dish.router, prefix="/dishes", tags=["dishes"])
api_router.include_router(order.router, prefix="/orders", tags=["orders"])
