from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import Sequence, Optional

from app.models.dish import Dish
from app.schemas.dish import DishCreate


class DishService:
    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализация сервиса блюд.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
        """
        self.session = session

    async def get_all(self) -> Sequence[Dish]:
        """
        Получить все блюда из базы данных.

        Returns:
            Sequence[Dish]: Список всех блюд.
        """
        result = await self.session.execute(select(Dish))
        return result.scalars().all()

    async def get_by_id(self, dish_id: int) -> Optional[Dish]:
        """
        Получить блюдо по его идентификатору.

        Args:
            dish_id (int): Идентификатор блюда.

        Returns:
            Optional[Dish]: Объект блюда, если найден, иначе None.
        """
        return await self.session.get(Dish, dish_id)

    async def create(self, dish_create: DishCreate) -> Dish:
        """
        Создать новое блюдо в базе данных.

        Args:
            dish_create (DishCreate): Данные для создания блюда.

        Raises:
            SQLAlchemyError: При ошибках при работе с базой данных.

        Returns:
            Dish: Созданное блюдо.
        """
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
        """
        Удалить блюдо по идентификатору.

        Args:
            dish_id (int): Идентификатор блюда для удаления.

        Raises:
            SQLAlchemyError: При ошибках при работе с базой данных.

        Returns:
            bool: True, если блюдо было удалено, False если не найдено.
        """
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
