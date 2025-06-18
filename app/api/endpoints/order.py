from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core import database
from app.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate
from app.services.order_service import OrderService

router = APIRouter()


@router.get("/", response_model=List[OrderRead])
async def get_orders(session: AsyncSession = Depends(database.get_db)):
    service = OrderService(session)
    return await service.get_all()


@router.post("/", response_model=OrderRead)
async def create_order(order: OrderCreate, session: AsyncSession = Depends(database.get_db)):
    service = OrderService(session)
    try:
        return await service.create(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}", status_code=204)
async def cancel_order(order_id: int, session: AsyncSession = Depends(database.get_db)):
    service = OrderService(session)
    try:
        success = await service.delete(order_id)
        if not success:
            raise HTTPException(status_code=404, detail="Заказ не найден")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{order_id}/status", response_model=OrderRead)
async def update_order_status(
        order_id: int, status_update: OrderStatusUpdate, session: AsyncSession = Depends(database.get_db)):
    service = OrderService(session)
    try:
        return await service.update_status(order_id, status_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
