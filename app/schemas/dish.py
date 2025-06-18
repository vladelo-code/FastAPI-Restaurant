from pydantic import BaseModel, Field, ConfigDict


class DishBase(BaseModel):
    name: str = Field(..., example="Пицца Маргарита")
    description: str | None = Field(None, example="Традиционная итальянская пицца с томатным соусом и сыром моцарелла")
    price: float = Field(..., gt=0, example=500.0)
    category: str = Field(..., example="Основные блюда")


class DishCreate(DishBase):
    pass


class DishRead(DishBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
