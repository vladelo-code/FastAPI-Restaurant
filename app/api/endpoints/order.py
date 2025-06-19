from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Sequence, List

from app.core import database
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate
from app.services.order_service import OrderService

router = APIRouter()


@router.get("/", response_model=List[OrderRead])
async def get_orders(session: Session = Depends(database.get_db)) -> Sequence[Order]:
    """
    Получить список всех заказов.

    Args:
        session (Session): Сессия базы данных.

    Returns:
        Sequence[Order]: Список заказов в формате Order.
    """
    service = OrderService(session)
    return await service.get_all()


@router.post("/", response_model=OrderRead)
async def create_order(order: OrderCreate, session: Session = Depends(database.get_db)) -> Order:
    """
    Создать новый заказ.

    Args:
        order (OrderCreate): Данные для создания заказа.
        session (Session): Сессия базы данных.

    Raises:
        HTTPException: При ошибках валидации данных (статус 400).

    Returns:
        Order: Созданный заказ.
    """
    service = OrderService(session)
    try:
        return await service.create(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}", status_code=204)
async def cancel_order(order_id: int, session: Session = Depends(database.get_db)) -> None:
    """
    Отменить (удалить) заказ по ID.

    Args:
        order_id (int): Идентификатор заказа.
        session (Session): Сессия базы данных.

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
                              session: Session = Depends(database.get_db)) -> Order:
    """
    Обновить статус заказа.

    Args:
        order_id (int): Идентификатор заказа.
        status_update (OrderStatusUpdate): Новое значение статуса.
        session (Session): Сессия базы данных.

    Raises:
        HTTPException: При ошибках валидации или невозможности обновления статуса (400).

    Returns:
        Order: Обновленный заказ.
    """
    service = OrderService(session)
    try:
        return await service.update_status(order_id, status_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
