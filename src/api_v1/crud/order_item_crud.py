from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from src.models import Order, OrderItem, Product

from src.api_v1.schemas import OrderItemRead, OrderItemUpdate, ProductRead

from src.api_v1.crud.base_crud import CRUD
from src.api_v1.crud.product_crud import crud_product
from src.api_v1.crud.serializer import serialize_order_item


class OrderItemCRUD(CRUD):
    async def create_order_item(self, session: AsyncSession, order: Order, item: OrderItem) -> OrderItemRead:
        product = await crud_product.get_product_by_name(session=session, product_name=item.product.name)
        if not product:
            product = await crud_product.create_product(session=session, product=item.product)

        new_order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            available=False,
            status='Created'
        )
        session.add(new_order_item)
        await session.commit()
        await session.refresh(new_order_item)
        order_item = await serialize_order_item(session=session, order_item=new_order_item)

        return order_item

    async def get_order_item(self, session: AsyncSession, order_item_id: int) -> OrderItemRead:
        item = await session.get(self.model, order_item_id)
        return item


crud_order_item = OrderItemCRUD(OrderItem)
