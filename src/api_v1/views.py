from typing import Annotated, List

from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession


from src.db_helper import get_async_session
from src.api_v1.schemas.provider import ProviderRead, ProviderCreate
from src.api_v1.schemas.product import ProductRead, ProductCreate
from src.api_v1.schemas.dealer import DealerCreate, DealerRead
from src.api_v1.schemas.order import OrderCreate, OrderItemRead, OrderRead

from src.api_v1.crud.product_crud import crud_product
from src.api_v1.crud.dealer_crud import crud_dealer
from src.api_v1.crud.order_crud import crud_order
from src.api_v1.crud.provider_crud import crud_provider

router = APIRouter(prefix='/api/v1', tags=['api_v1'])


@router.get('/get_dealer_orders/{dealer_id}/')
async def get_dealer_orders_by_id(dealer_id: int, session: AsyncSession = Depends(get_async_session)):
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
                                              order=order,)
    return new_order
