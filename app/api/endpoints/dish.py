from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Sequence, List, Dict

from app.schemas.dish import DishCreate, DishRead
from app.models.dish import Dish
from app.core import database
from app.services.dish_service import DishService

router = APIRouter()


@router.get("/", response_model=List[DishRead])
async def get_dishes(session: Session = Depends(database.get_db)) -> Sequence[Dish]:
    """
    Получить список всех блюд.

    Args:
        session (Session): Сессия базы данных.

    Returns:
        Sequence[Dish]: Список всех блюд в базе данных.
    """
    service = DishService(session)
    return await service.get_all()


@router.post("/", response_model=DishRead)
async def create_dish(dish: DishCreate, session: Session = Depends(database.get_db)) -> Dish:
    """
    Создать новое блюдо.

    Args:
        dish (DishCreate): Данные для создания блюда.
        session (Session): Сессия базы данных.

    Returns:
        Dish: Созданное блюдо с подробной информацией.
    """
    service = DishService(session)
    return await service.create(dish)


@router.delete("/{dish_id}")
async def delete_dish(dish_id: int, session: Session = Depends(database.get_db)) -> Dict[str, str]:
    """
    Удалить блюдо по ID.

    Args:
        dish_id (int): Идентификатор блюда для удаления.
        session (Session): Сессия базы данных.

    Raises:
        HTTPException: Если блюдо с указанным ID не найдено (404).

    Returns:
        Dict[str, str]: Сообщение об успешном удалении блюда.
    """
    service = DishService(session)
    success = await service.delete(dish_id)

    if not success:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    return {"detail": "Блюдо удалено"}
