from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from src.api_v1.schemas.dealer import DealerCreate, DealerRead
from src.api_v1.schemas.product import ProductCreate, ProductRead


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


