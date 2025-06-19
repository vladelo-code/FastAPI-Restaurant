from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import datetime
from typing import Sequence, List

from app.models.order import Order
from app.models.dish import Dish
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.core.logger import logger


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
        logger.info("Получение списка всех заказов")
        result = self.session.execute(select(Order).options(selectinload(Order.dishes)))
        orders = result.scalars().all()
        logger.debug(f"Найдено заказов: {len(orders)}")
        return orders

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
        logger.info(f"Создание нового заказа для клиента: {order_create.customer_name}")
        dishes = []
        for dish_id in order_create.dish_ids:
            dish = self.session.get(Dish, dish_id)
            if not dish:
                logger.warning(f"Блюдо с ID {dish_id} не найдено при создании заказа")
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

        result = self.session.execute(
            select(Order)
            .options(selectinload(Order.dishes))
            .where(Order.id == order.id)
        )
        order = result.scalars().first()

        logger.debug(f"Заказ создан с ID {order.id}")
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
        logger.info(f"Попытка удалить заказ с ID: {order_id}")
        order = self.session.get(Order, order_id)
        if not order:
            logger.warning(f"Заказ с ID {order_id} не найден для удаления")
            return False
        if order.status != "в обработке":
            logger.warning(f"Попытка удалить заказ с ID {order_id}, но его статус: {order.status}")
            raise ValueError("Отменить заказ можно только в статусе 'в обработке'")
        self.session.delete(order)
        self.session.commit()
        logger.debug(f"Заказ с ID {order_id} успешно удалён")
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
        logger.info(f"Обновление статуса заказа ID {order_id} -> {status_update.status}")
        result = self.session.execute(
            select(Order).options(selectinload(Order.dishes)).where(Order.id == order_id)
        )
        order = result.scalars().first()

        if not order:
            logger.error(f"Заказ с ID {order_id} не найден при обновлении статуса")
            raise HTTPException(status_code=404, detail="Заказ не найден")

        current_status = order.status.strip().lower()
        new_status = status_update.status.strip().lower()

        allowed = self.allowed_status_transitions.get(current_status, [])

        if not allowed:
            logger.warning(f"Заказ с ID {order_id} уже завершён, статус нельзя изменить")
            raise HTTPException(
                status_code=400,
                detail=f"Заказ уже завершен!"
            )

        if new_status not in allowed:
            logger.warning(
                f"Недопустимый переход статуса для заказа ID {order_id}: {current_status} -> {new_status}"
            )
            raise HTTPException(
                status_code=400,
                detail=f"Нельзя перейти из статуса '{current_status}' в '{new_status}'. "
                       f"Допустимые переходы: '{allowed[0]}'!"
            )

        order.status = new_status
        self.session.commit()
        self.session.refresh(order)

        logger.debug(f"Статус заказа ID {order_id} обновлён на '{new_status}'")
        return order
