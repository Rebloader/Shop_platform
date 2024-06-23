from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
if TYPE_CHECKING:
    from .order import Order


class Dealer(Base):
    __tablename__ = 'dealer'

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    orders: Mapped[List['Order']] = relationship('Order', back_populates='dealer')
