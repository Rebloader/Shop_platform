from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.crud.product_crud import crud_product
from src.api_v1.schemas.dealer import DealerRead
from src.api_v1.schemas.order import OrderItemRead, OrderRead
from src.api_v1.schemas.product import ProductRead
from src.models import OrderItem, Order


async def serialize_order_item(session: AsyncSession, order_item: OrderItem) -> OrderItemRead:
    product_info = await crud_product.get_item_by_id(session=session, id_=order_item.product_id)
    return OrderItemRead(
        id=order_item.id,
        quantity=order_item.quantity,
        product=ProductRead(id=product_info.id, name=product_info.name, price=product_info.price),
        provider_id=order_item.provider_id,
        available=order_item.available,
        delivery_time=order_item.delivery_time,
        total_price=(product_info.price*order_item.quantity)
    )


async def serialize_order(session: AsyncSession, order: Order, dealer_info: DealerRead) -> OrderRead:
    order_items: list[OrderItemRead] = []
    for order_item in order.items:
        order_item_info = await serialize_order_item(session, order_item)
        order_items.append(order_item_info)
    return OrderRead(
        id=order.id,
        status=order.status,
        dealer=dealer_info,
        created_at=order.created_at,
        items=order_items,
    )
