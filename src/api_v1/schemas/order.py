from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    id: int
    provider_id: Optional[int]
    available: bool
    delivery_time: Optional[datetime]


class OrderBase(BaseModel):
    dealer_id: int
    status: str


class OrderCreate(OrderBase):
    items: List['OrderItemCreate']


class OrderRead(OrderBase):
    id: int
    created_at: datetime
    items: List['OrderItemRead']


