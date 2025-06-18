from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.order import Order
from app.models.dish import Dish
from app.schemas.order import OrderCreate, OrderStatusUpdate
from datetime import datetime


class OrderService:
    allowed_status_transitions = {
        "в обработке": ["готовится"],
        "готовится": ["доставляется"],
        "доставляется": ["завершен"],
        "завершен": [],
    }

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(select(Order))
        return result.scalars().all()

    async def create(self, order_create: OrderCreate):
        # Проверяем, что все блюда существуют
        dishes = []
        for dish_id in order_create.dish_ids:
            dish = await self.session.get(Dish, dish_id)
            if not dish:
                raise ValueError(f"Блюдо с id={dish_id} не найдено")
            dishes.append(dish)

        order = Order(
            customer_name=order_create.customer_name,
            order_time=datetime.utcnow(),
            status="в обработке",
            dishes=dishes,
        )
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def delete(self, order_id: int):
        order = await self.session.get(Order, order_id)
        if not order:
            return False
        if order.status != "в обработке":
            raise ValueError("Отменить заказ можно только в статусе 'в обработке'")
        await self.session.delete(order)
        await self.session.commit()
        return True

    async def update_status(self, order_id: int, status_update: OrderStatusUpdate):
        order = await self.session.get(Order, order_id)
        if not order:
            raise ValueError("Заказ не найден")

        current_status = order.status
        new_status = status_update.status

        allowed = self.allowed_status_transitions.get(current_status, [])
        if new_status not in allowed:
            raise ValueError(f"Статус может изменяться только по цепочке: {self.allowed_status_transitions}")

        order.status = new_status
        await self.session.commit()
        await self.session.refresh(order)
        return order
