from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from base_crud import CRUD
from src.models import Order, OrderItem
from src.api_v1.schemas.order import OrderRead, OrderItemRead, OrderItemCreate, OrderCreate


class OrderCRUD(CRUD):
    pass