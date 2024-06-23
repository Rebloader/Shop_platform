from typing import List

from sqlalchemy import nteger, String, ForeignKey, UniqueConstraint, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.order import OrderItem


class Provider(Base):
    __tablename__ = 'provider'

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    order_items: Mapped[List['OrderItem']] = relationship('OrderItem', back_populates='provider')