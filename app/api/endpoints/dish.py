from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.dish import DishCreate, DishRead
from app.core import database
from app.services.dish_service import DishService

router = APIRouter(prefix="/dishes", tags=["Dishes"])


@router.get("/", response_model=list[DishRead])
async def get_dishes(session: AsyncSession = Depends(database.get_db)):
    service = DishService(session)
    return await service.get_all()


@router.post("/", response_model=DishRead)
async def create_dish(dish: DishCreate, session: AsyncSession = Depends(database.get_db)):
    service = DishService(session)
    return await service.create(dish)


@router.delete("/{dish_id}")
async def delete_dish(dish_id: int, session: AsyncSession = Depends(database.get_db)):
    service = DishService(session)
    success = await service.delete(dish_id)
    if not success:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    return {"detail": "Блюдо удалено"}
