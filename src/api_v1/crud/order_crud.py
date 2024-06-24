from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api_v1.schemas.dealer import DealerRead
from src.api_v1.schemas.product import ProductRead
from src.models import Order, OrderItem, Product, Dealer
from src.api_v1.crud.base_crud import CRUD
from src.api_v1.crud.product_crud import crud_product
from src.api_v1.crud.provider_crud import crud_provider
from src.api_v1.crud.dealer_crud import crud_dealer
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

        order_items: list[OrderItemRead] = []
        for order_item in order.items:
            product = await crud_product.get_product_by_name(session=session, product_name=order_item.product.name)
            if not product:
                product = await crud_product.create_product(session=session, product=order_item.product)

            new_order_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=order_item.quantity,
                available=False,
                status='Created'
            )
            session.add(new_order_item)
            await session.commit()
            await session.refresh(new_order_item)

            order_item_read = OrderItemRead(
                id=new_order_item.id,
                product=ProductRead(id=product.id, name=product.name, price=product.price),
                quantity=new_order_item.quantity,
                provider_id=new_order_item.provider_id,
                available=new_order_item.available,
                delivery_time=new_order_item.delivery_time
            )
            order_items.append(order_item_read)

        order_read = OrderRead(
            id=new_order.id,
            dealer=DealerRead(id=new_order.dealer_id, name=order.dealer.name, email=order.dealer.email,
                              phone=order.dealer.phone, address=order.dealer.address),
            created_at=new_order.created_at,
            status=new_order.status,
            items=order_items
        )

        return order_read

    async def get_dealer_orders(self, session: AsyncSession, dealer_id: int) -> list[OrderRead]:
        stmt = (select(self.model)
                .options(selectinload(self.model.items))
                .where(self.model.dealer_id == dealer_id))

        result = await session.execute(stmt)
        result = result.scalars().all()

        dealer_info = await crud_dealer.get_item_by_id(session=session, id_=dealer_id)

        orders_result: list[OrderRead] = []
        for order in result:
            order_items: list[OrderItemRead] = []
            # list_order_item = await session.execute(select(OrderItem).where(OrderItem.order_id == order.id))
            for order_item in order.items:
                product_info = await crud_product.get_item_by_id(session=session, id_=order_item.product_id)
                order_item_info = OrderItemRead(
                    id=order_item.order_id,
                    quantity=order_item.quantity,
                    product=ProductRead(id=product_info.id, name=product_info.name, price=product_info.price),
                    provider_id=order_item.provider_id,
                    available=order_item.available,
                    delivery_time=order_item.delivery_time,
                )
                order_items.append(order_item_info)
            order_read = OrderRead(
                id=order.id,
                status=order.status,
                dealer=DealerRead(id=dealer_info.id, name=dealer_info.name, email=dealer_info.email,
                                  address=dealer_info.address, phone=dealer_info.phone, ),
                created_at=order.created_at,
                items=order_items,
            )
            orders_result.append(order_read)

        return orders_result

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
