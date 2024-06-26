from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api_v1.schemas.dealer import DealerRead
from src.api_v1.schemas.product import ProductRead
from src.models import Order, OrderItem, Product
from src.api_v1.crud.base_crud import CRUD
from src.api_v1.crud.product_crud import crud_product
from src.api_v1.crud.provider_crud import crud_provider
from src.api_v1.crud.dealer_crud import crud_dealer
from src.api_v1.schemas.order import OrderRead, OrderItemRead, OrderItemCreate, OrderCreate, OrderItemUpdate
from src.api_v1.crud.serializer import serialize_order_item, serialize_order


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
                delivery_time=new_order_item.delivery_time,
                total_price=(product.price * new_order_item.quantity)
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

    async def get_order_by_id(self, order_id: int, session: AsyncSession) -> OrderRead:
        order = await session.execute(select(self.model).where(self.model.id == order_id).
                                      options(selectinload(self.model.items)))
        order = order.scalar_one_or_none()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        dealer_db = await crud_dealer.get_item_by_id(session=session, id_=order.dealer_id)
        dealer = DealerRead(id=dealer_db.id, name=dealer_db.name, email=dealer_db.email,
                            phone=dealer_db.phone, address=dealer_db.address)
        await session.refresh(order, attribute_names=['items'])

        order_read = await serialize_order(session, order, dealer)
        return order_read

    async def get_dealer_orders(self, session: AsyncSession, dealer_id: int) -> list[OrderRead]:
        stmt = (select(self.model)
                .options(selectinload(self.model.items))
                .where(self.model.dealer_id == dealer_id))

        result = await session.execute(stmt)
        result = result.scalars().all()

        dealer_info = await crud_dealer.get_item_by_id(session=session, id_=dealer_id)

        dealer_to_read = DealerRead(id=dealer_info.id, name=dealer_info.name, email=dealer_info.email,
                                    phone=dealer_info.phone, address=dealer_info.address)
        result = [await serialize_order(session, order, dealer_to_read) for order in result]
        return result

    async def update_order_status(self, session: AsyncSession, order_id: int):
        order = await session.get(self.model, order_id)
        order.status = 'In process'
        await session.commit()
        await session.refresh(order)

    async def update_order_item(self, session: AsyncSession, order_item: OrderItemUpdate,
                                order_item_id: int, product_id: int) -> OrderItemRead:
        db_order_item = await session.get(OrderItem, order_item_id)
        if not db_order_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        product_update = await session.get(Product, product_id)
        product_update.price = order_item.product.price
        await session.commit()
        await session.refresh(product_update)
        await self.update_order_status(session, db_order_item.order_id)

        db_order_item.provider_id = order_item.provider_id
        db_order_item.available = order_item.available
        db_order_item.delivery_time = order_item.delivery_time
        db_order_item.quantity = order_item.quantity
        db_order_item.status = 'In process'
        db_order_item.total_price = product_update.price * order_item.quantity

        await session.commit()
        await session.refresh(db_order_item)
        return OrderItemRead(
            id=db_order_item.id,
            product=ProductRead(id=product_update.id, name=product_update.name, price=product_update.price),
            quantity=db_order_item.quantity,
            provider_id=db_order_item.provider_id,
            available=db_order_item.available,
            delivery_time=db_order_item.delivery_time,
            total_price=db_order_item.total_price
        )

    async def close_order(self, session: AsyncSession, new_status: str, order_id: int) -> list[OrderRead]:
        order_to_update = await session.get(self.model, order_id)
        if not order_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        order_to_update.status = new_status

        await session.commit()
        await session.refresh(order_to_update)
        order_to_read = await self.get_dealer_orders(session=session, dealer_id=order_to_update.dealer_id)
        return order_to_read


crud_order = OrderCRUD(Order)
