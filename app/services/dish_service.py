from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import Sequence, Optional

from app.models.dish import Dish
from app.schemas.dish import DishCreate
from app.core.logger import logger


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
        logger.info("Получение всех блюд из базы данных")
        result = self.session.execute(select(Dish))
        dishes = result.scalars().all()
        logger.debug(f"Найдено {len(dishes)} блюд")
        return dishes

    async def get_by_id(self, dish_id: int) -> Optional[Dish]:
        """
        Получить блюдо по его идентификатору.

        Args:
            dish_id (int): Идентификатор блюда.

        Returns:
            Optional[Dish]: Объект блюда, если найден, иначе None.
        """
        logger.info(f"Получение блюда по ID: {dish_id}")
        dish = self.session.get(Dish, dish_id)
        if dish:
            logger.debug(f"Блюдо найдено: {dish.name}")
        else:
            logger.warning(f"Блюдо с ID {dish_id} не найдено")
        return dish

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
        logger.info(f"Создание нового блюда: {dish_create.name}")
        dish = Dish(**dish_create.model_dump())
        self.session.add(dish)
        try:
            self.session.commit()
            self.session.refresh(dish)
            logger.debug(f"Блюдо успешно создано с ID: {dish.id}")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Ошибка при создании блюда: {e}")
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
        logger.info(f"Удаление блюда с ID: {dish_id}")
        dish = await self.get_by_id(dish_id)
        if dish:
            self.session.delete(dish)
            try:
                self.session.commit()
                logger.debug(f"Блюдо с ID {dish_id} успешно удалено")
            except SQLAlchemyError as e:
                self.session.rollback()
                logger.error(f"Ошибка при удалении блюда с ID {dish_id}: {e}")
                raise
            return True
        logger.warning(f"Попытка удалить несуществующее блюдо с ID {dish_id}")
        return False
