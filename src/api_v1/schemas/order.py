from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    provider_id: int
    available: bool
    delivery_time: Optional[datetime]


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    id: int


class OrderBase(BaseModel):
    dealer_id: int
    created_at: datetime
    status: str


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItemRead]


