from typing import List, TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
if TYPE_CHECKING:
    from .order import OrderItem


class Product(Base):
    __tablename__ = 'product'

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    price: Mapped[str] = mapped_column(Integer, nullable=True)

    order_items: Mapped[List['OrderItem']] = relationship('OrderItem', back_populates='product')
