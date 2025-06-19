from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import datetime
from typing import Sequence, List

from app.models.order import Order
from app.models.dish import Dish
from app.schemas.order import OrderCreate, OrderStatusUpdate


class OrderService:
    allowed_status_transitions = {
        "в обработке": ["готовится"],
        "готовится": ["доставляется"],
        "доставляется": ["завершен"],
        "завершен": [],
    }

    def __init__(self, session: Session) -> None:
        """
        Инициализация сервиса заказов.

        Args:
            session (Session): Сессия базы данных.
        """
        self.session = session

    async def get_all(self) -> Sequence[Order]:
        """
        Получить все заказы с предзагрузкой связанных блюд.

        Returns:
            List[Order]: Список всех заказов.
        """
        result = self.session.execute(select(Order).options(selectinload(Order.dishes)))
        return result.scalars().all()

    async def create(self, order_create: OrderCreate) -> Order:
        """
        Создать новый заказ.

        Args:
            order_create (OrderCreate): Данные для создания заказа.

        Raises:
            ValueError: Если какое-либо блюдо не найдено.

        Returns:
            Order: Созданный заказ с загруженными блюдами.
        """
        dishes = []
        for dish_id in order_create.dish_ids:
            dish = self.session.get(Dish, dish_id)
            if not dish:
                raise ValueError(f"Блюдо с id={dish_id} не найдено")
            dishes.append(dish)

        order = Order(
            customer_name=order_create.customer_name,
            order_time=datetime.now(),
            status="в обработке",
            dishes=dishes,
        )
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)

        # Явно загружаем блюда вместе с заказом
        result = self.session.execute(
            select(Order)
            .options(selectinload(Order.dishes))
            .where(Order.id == order.id)
        )
        order = result.scalars().first()

        return order

    async def delete(self, order_id: int) -> bool:
        """
        Удалить заказ по идентификатору, если он в статусе "в обработке".

        Args:
            order_id (int): Идентификатор заказа для удаления.

        Raises:
            ValueError: Если заказ не в статусе "в обработке".

        Returns:
            bool: True, если заказ удалён, иначе False.
        """
        order = self.session.get(Order, order_id)
        if not order:
            return False
        if order.status != "в обработке":
            raise ValueError("Отменить заказ можно только в статусе 'в обработке'")
        self.session.delete(order)
        self.session.commit()
        return True

    async def update_status(self, order_id: int, status_update: OrderStatusUpdate) -> Order:
        """
        Обновить статус заказа с проверкой допустимых переходов.

        Args:
            order_id (int): Идентификатор заказа.
            status_update (OrderStatusUpdate): Новый статус заказа.

        Raises:
            HTTPException: Если заказ не найден или переход статуса недопустим.

        Returns:
            Order: Заказ с обновлённым статусом.
        """
        result = self.session.execute(
            select(Order).options(selectinload(Order.dishes)).where(Order.id == order_id)
        )
        order = result.scalars().first()

        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")

        current_status = order.status.strip().lower()
        new_status = status_update.status.strip().lower()

        allowed = self.allowed_status_transitions.get(current_status, [])

        if not allowed:
            raise HTTPException(
                status_code=400,
                detail=f"Заказ уже завершен!"
            )

        if new_status not in allowed:
            raise HTTPException(
                status_code=400,
                detail=f"Нельзя перейти из статуса '{current_status}' в '{new_status}'. "
                       f"Допустимые переходы: '{allowed[0]}'!"
            )

        order.status = new_status
        self.session.commit()
        self.session.refresh(order)

        return order
