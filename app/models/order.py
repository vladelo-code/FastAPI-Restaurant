from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

order_dishes = Table(
    "order_dishes",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("dish_id", Integer, ForeignKey("dishes.id"), primary_key=True),
)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    order_time = Column(DateTime, default=datetime.now)
    status = Column(String, default="в обработке")

    dishes = relationship("Dish", secondary=order_dishes, backref="orders")
