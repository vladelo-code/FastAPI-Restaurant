from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.dish import Dish
from app.schemas.dish import DishCreate
from typing import Sequence, Optional


class DishService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> Sequence[Dish]:
        result = await self.session.execute(select(Dish))
        return result.scalars().all()

    async def get_by_id(self, dish_id: int) -> Optional[Dish]:
        return await self.session.get(Dish, dish_id)

    async def create(self, dish_create: DishCreate) -> Dish:
        dish = Dish(**dish_create.model_dump())
        self.session.add(dish)
        try:
            await self.session.commit()
            await self.session.refresh(dish)
        except SQLAlchemyError:
            await self.session.rollback()
            raise
        return dish

    async def delete(self, dish_id: int) -> bool:
        dish = await self.get_by_id(dish_id)
        if dish:
            await self.session.delete(dish)
            try:
                await self.session.commit()
            except SQLAlchemyError:
                await self.session.rollback()
                raise
            return True
        return False
