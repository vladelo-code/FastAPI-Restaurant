from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core import database
from app.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate
from app.services.order_service import OrderService

router = APIRouter()


@router.get("/", response_model=List[OrderRead])
async def get_orders(session: AsyncSession = Depends(database.get_db)) -> List[OrderRead]:
    """
    Получить список всех заказов.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        List[OrderRead]: Список заказов в формате OrderRead.
    """
    service = OrderService(session)
    return await service.get_all()


@router.post("/", response_model=OrderRead)
async def create_order(order: OrderCreate, session: AsyncSession = Depends(database.get_db)) -> OrderRead:
    """
    Создать новый заказ.

    Args:
        order (OrderCreate): Данные для создания заказа.
        session (AsyncSession): Асинхронная сессия базы данных.

    Raises:
        HTTPException: При ошибках валидации данных (статус 400).

    Returns:
        OrderRead: Созданный заказ.
    """
    service = OrderService(session)
    try:
        return await service.create(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}", status_code=204)
async def cancel_order(order_id: int, session: AsyncSession = Depends(database.get_db)) -> None:
    """
    Отменить (удалить) заказ по ID.

    Args:
        order_id (int): Идентификатор заказа.
        session (AsyncSession): Асинхронная сессия базы данных.

    Raises:
        HTTPException: Если заказ не найден (404) или другая ошибка (400).
    """
    service = OrderService(session)
    try:
        success = await service.delete(order_id)
        if not success:
            raise HTTPException(status_code=404, detail="Заказ не найден")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{order_id}/status", response_model=OrderRead)
async def update_order_status(order_id: int, status_update: OrderStatusUpdate,
                              session: AsyncSession = Depends(database.get_db)) -> OrderRead:
    """
    Обновить статус заказа.

    Args:
        order_id (int): Идентификатор заказа.
        status_update (OrderStatusUpdate): Новое значение статуса.
        session (AsyncSession): Асинхронная сессия базы данных.

    Raises:
        HTTPException: При ошибках валидации или невозможности обновления статуса (400).

    Returns:
        OrderRead: Обновленный заказ.
    """
    service = OrderService(session)
    try:
        return await service.update_status(order_id, status_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
