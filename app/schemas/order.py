from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List
from datetime import datetime

from app.schemas.dish import DishRead


class OrderBase(BaseModel):
    customer_name: str = Field(..., example="Иван Иванов")
    status: str = Field(default="в обработке", example="в обработке")


class OrderCreate(BaseModel):
    customer_name: str = Field(..., example="Иван Иванов")
    dish_ids: List[int] = Field(..., example=[1, 2])


class OrderRead(OrderBase):
    id: int
    order_time: datetime
    dishes: List[DishRead]

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    status: str = Field(..., example="готовится")

    @field_validator("status")
    def validate_status(cls, v):
        allowed_statuses = ["в обработке", "готовится", "доставляется", "завершен"]
        if v not in allowed_statuses:
            raise ValueError(f"Статус должен быть одним из {allowed_statuses}")
        return v
