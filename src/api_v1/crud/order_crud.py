from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from provider_crud import crud_provider
from src.models import Order, OrderItem
from src.api_v1.crud.base_crud import CRUD
from src.api_v1.schemas.order import OrderRead, OrderItemRead, OrderItemCreate, OrderCreate


class OrderCRUD(CRUD):
    async def create_order(self, session: AsyncSession, order: OrderCreate) -> OrderRead:
        order = self.model(
            dealer_id=order.dealer_id,
            created_at=datetime.now(),
            status=order.status,
        )
        session.add(order)
        await session.commit()
        await session.refresh(order)

        for item in order.items:
            new_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                available=False,
            )
            session.add(new_item)
        await session.commit()
        await session.refresh(order)
        return order

    async def update_order_item_provider(self, session: AsyncSession, order_item_id: int,
                                         provider_name: str, available: bool,
                                         delivery_time: datetime, status: str) -> Optional[OrderItemRead]:
        provider = await crud_provider.get_provider_by_name(name=provider_name, session=session)
        order_item = await session.get(OrderItem, order_item_id)
        if order_item:
            order_item.provider_id = provider.id
            order_item.available = available
            order_item.delivery_time = delivery_time
            order_item.status = status
            await session.commit()
            await session.refresh(order_item)
        return order_item


crud_order = OrderCRUD(Order)
