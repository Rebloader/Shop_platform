from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.crud.dealer_crud import crud_dealer
from src.api_v1.crud.order_crud import crud_order
from src.api_v1.crud.order_item_crud import crud_order_item
from src.api_v1.crud.serializer import serialize_order_item
from src.api_v1.crud.product_crud import crud_product

from src.api_v1.schemas import OrderCreate, OrderRead, OrderItemRead, OrderItemUpdate
from src.db_helper import get_async_session

router = APIRouter(prefix='/order', tags=["Orders"])


@router.post('/create/', response_model=OrderRead)
async def create_order(order: OrderCreate,
                       session: Annotated[AsyncSession, Depends(get_async_session)]):
    dealer = await crud_dealer.get_dealer_by_name(session=session,
                                                  dealer_name=order.dealer.name)
    if not dealer:
        dealer = await crud_dealer.create_new_dealer(session=session,
                                                     new_dealer=order.dealer)

    new_order = await crud_order.create_order(session=session,
                                              dealer_id=dealer.id,
                                              order=order)
    return new_order


@router.get('/order_item/{order_item_id}/', response_model=OrderItemRead)
async def get_order_item_info(order_item_id: int,
                              session: Annotated[AsyncSession, Depends(get_async_session)]):
    order_item = await crud_order_item.get_order_item(session=session, order_item_id=order_item_id)
    if not order_item:
        raise HTTPException(404, 'Order item not found')
    result = await serialize_order_item(session=session, order_item=order_item)
    return result


@router.patch('/order_item/change/{order_item_id}/', response_model=OrderItemRead)
async def change_order_item_info(order_item_id: int,
                                 order_item: OrderItemUpdate,
                                 session: Annotated[AsyncSession, Depends(get_async_session)]):
    product = await crud_product.get_product_by_name(session=session, product_name=order_item.product.name)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    updated_order_item = await crud_order.update_order_item(session=session, order_item=order_item,
                                                            order_item_id=order_item_id,
                                                            product_id=product.id)
    return updated_order_item


@router.patch('/change_status/{order_id}/', response_model=list[OrderRead])
async def change_order_status(order_id: int, order_status: str,
                              session: Annotated[AsyncSession, Depends(get_async_session)]):
    orders = await crud_order.close_order(session=session, new_status=order_status, order_id=order_id)
    return orders
