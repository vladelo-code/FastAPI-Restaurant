from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import Sequence, Optional

from app.models.dish import Dish
from app.schemas.dish import DishCreate


class DishService:
    def __init__(self, session: Session) -> None:
        """
        Инициализация сервиса блюд.

        Args:
            session (Session): Сессия базы данных.
        """
        self.session = session

    async def get_all(self) -> Sequence[Dish]:
        """
        Получить все блюда из базы данных.

        Returns:
            Sequence[Dish]: Список всех блюд.
        """
        result = self.session.execute(select(Dish))
        return result.scalars().all()

    async def get_by_id(self, dish_id: int) -> Optional[Dish]:
        """
        Получить блюдо по его идентификатору.

        Args:
            dish_id (int): Идентификатор блюда.

        Returns:
            Optional[Dish]: Объект блюда, если найден, иначе None.
        """
        return self.session.get(Dish, dish_id)

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
            self.session.commit()
            self.session.refresh(dish)
        except SQLAlchemyError:
            self.session.rollback()
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
            self.session.delete(dish)
            try:
                self.session.commit()
            except SQLAlchemyError:
                self.session.rollback()
                raise
            return True
        return False
