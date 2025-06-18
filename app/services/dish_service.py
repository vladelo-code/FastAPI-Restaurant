from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.dish import Dish
from app.schemas.dish import DishCreate


class DishService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(select(Dish))
        return result.scalars().all()

    async def create(self, dish_create: DishCreate):
        dish = Dish(**dish_create.model_dump())
        self.session.add(dish)
        await self.session.commit()
        await self.session.refresh(dish)
        return dish

    async def delete(self, dish_id: int):
        dish = await self.session.get(Dish, dish_id)
        if dish:
            await self.session.delete(dish)
            await self.session.commit()
            return True
        return False
