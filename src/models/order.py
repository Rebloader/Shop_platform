from datetime import datetime
from typing import List

from sqlalchemy import nteger, String, ForeignKey, UniqueConstraint, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.dealer import Dealer
from src.models.product import Product
from src.models.provider import Provider


class Order(Base):
    __tablename__ = 'order'

    dealer_id: Mapped[int] = mapped_column(ForeignKey('dealer.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    status: Mapped[str] = mapped_column(String, nullable=False)

    items: Mapped[List['OrderItem']] = relationship('OrderItem', back_populates='order')
    dealer: Mapped['Dealer'] = relationship('Dealer', back_populates='orders')


class OrderItem(Base):
    __tablename__ = 'order_item'

    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    provider_id: Mapped[int] = mapped_column(ForeignKey('provider.id'))

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    delivery_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)

    product: Mapped['Product'] = relationship('Product', back_populates='order_items')
    order: Mapped['Order'] = relationship('Order', back_populates='items')
    provider: Mapped['Provider'] = relationship('Provider', back_populates='order_items')
