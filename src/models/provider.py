from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
if TYPE_CHECKING:
    from .order import OrderItem


class Provider(Base):
    __tablename__ = 'provider'

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    order_items: Mapped[List['OrderItem']] = relationship('OrderItem', back_populates='provider')