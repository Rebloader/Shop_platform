from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .dealer import DealerCreate, DealerRead
from .product import ProductCreate, ProductRead, ProductUpdate


class OrderItemBase(BaseModel):
    quantity: int


class OrderItemCreate(OrderItemBase):
    product: ProductCreate


class OrderItemRead(OrderItemBase):
    id: int
    product: ProductRead
    provider_id: Optional[int]
    available: bool
    delivery_time: Optional[datetime]
    total_price: int


class OrderItemUpdate(OrderItemBase):
    provider_id: int = Field(..., gt=0, le=99)
    product: ProductUpdate
    available: bool = True
    delivery_time: datetime


class OrderBase(BaseModel):
    status: str


class OrderCreate(OrderBase):
    items: List['OrderItemCreate']
    dealer: DealerCreate


class OrderRead(OrderBase):
    id: int
    dealer: DealerRead
    created_at: datetime
    items: List['OrderItemRead']


