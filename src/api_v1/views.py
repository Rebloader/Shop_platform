from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_helper import get_async_session
from src.api_v1.schemas.provider import ProviderRead, ProviderCreate
from src.api_v1.schemas.order import OrderCreate, OrderItemRead, OrderRead, OrderItemUpdate

from src.api_v1.crud.product_crud import crud_product
from src.api_v1.crud.dealer_crud import crud_dealer
from src.api_v1.crud.order_crud import crud_order
from src.api_v1.crud.provider_crud import crud_provider

from src.utils.convert_files.base_serializer import serialized_for_output
from src.utils.convert_files.converter_to_excel import create_excel_file_with_order_info

router = APIRouter(prefix='/api/v1', tags=['api_v1'])


@router.get('/get_all_dealer/')
async def get_all_dealers(session: Annotated[AsyncSession, Depends(get_async_session)]):
    dealers = await crud_dealer.get_dealer_list(session=session)
    return dealers


@router.get('/get_serializer_file/')
async def get_serializer_file(order_id: int, session: Annotated[AsyncSession, Depends(get_async_session)]):
    order = await crud_order.get_order_by_id(session=session, order_id=order_id)
    dict_to_msg = await serialized_for_output(order=order)
    file_path = await create_excel_file_with_order_info(dict_to_msg)
    return {'dict': dict_to_msg, 'file_path': file_path}


@router.get('/get_dealer_orders/{dealer_id}/', response_model=list[OrderRead])
async def get_dealer_orders_by_id(dealer_id: int, session: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await crud_order.get_dealer_orders(session=session, dealer_id=dealer_id)
    return result


@router.post('/add_provider/', response_model=ProviderRead)
async def add_provider(provider: ProviderCreate,
                       session: Annotated[AsyncSession, Depends(get_async_session)]):
    provider = await crud_provider.create_provider(session=session, provider=provider)
    return provider


@router.post('/create_order/', response_model=OrderRead)
async def create_order(order: OrderCreate,
                       session: Annotated[AsyncSession, Depends(get_async_session)]):
    dealer = await crud_dealer.get_dealer_by_name(session=session,
                                                  dealer_name=order.dealer.name)
    if not dealer:
        dealer = await crud_dealer.create_new_dealer(session=session,
                                                     new_dealer=order.dealer)

    new_order = await crud_order.create_order(session=session,
                                              dealer_id=dealer.id,
                                              status=order.status,
                                              order=order)
    return new_order


@router.patch('/change_order_item_info/{order_item_id}', response_model=OrderItemRead)
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


@router.patch('/change_order_status/{order_id}', response_model=list[OrderRead])
async def change_order_status(order_id: int, order_status: str,
                              session: Annotated[AsyncSession, Depends(get_async_session)]):
    orders = await crud_order.close_order(session=session, new_status=order_status, order_id=order_id)
    return orders
