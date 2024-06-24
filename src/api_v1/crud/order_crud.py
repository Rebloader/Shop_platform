from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.schemas.product import ProductRead
from src.models import Order, OrderItem
from src.api_v1.crud.base_crud import CRUD
from src.api_v1.crud.product_crud import crud_product
from src.api_v1.crud.provider_crud import crud_provider
from src.api_v1.schemas.order import OrderRead, OrderItemRead, OrderItemCreate, OrderCreate


class OrderCRUD(CRUD):
    async def create_order(self, session: AsyncSession,
                           dealer_id: int,
                           status: str,
                           order: OrderCreate) -> OrderRead:
        new_order = self.model(
            dealer_id=dealer_id,
            created_at=datetime.now(),
            status=status,
        )
        session.add(new_order)
        await session.commit()
        await session.refresh(new_order)

        order_items = order.items
        for order_item in order_items:
            product = await crud_product.get_product_by_name(session=session,
                                                             product_name=order_item.product.name)
            if not product:
                product = await crud_product.create_product(session=session,
                                                            product=order_item.product)
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=order_item.quantity,
                available=False,
                status='Created'
            )
            session.add(order_item)
        await session.commit()
        await session.refresh(new_order)

        return new_order

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
