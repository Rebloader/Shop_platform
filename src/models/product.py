from typing import List

from sqlalchemy import nteger, String, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.order import OrderItem


class Product(Base):
    __tablename__ = 'product'

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    price: Mapped[str] = mapped_column(Integer, nullable=False)

    order_items: Mapped[List['OrderItem']] = relationship('OrderItem', back_populates='product')
