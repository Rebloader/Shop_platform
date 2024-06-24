from typing import Annotated, List

from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_helper import get_async_session

from src.api_v1.schemas.product import ProductRead, ProductCreate
from src.api_v1.schemas.dealer import DealerCreate, DealerRead
from src.api_v1.schemas.order import OrderCreate, OrderItemRead, OrderRead

from src.api_v1.crud.product_crud import crud_product
from src.api_v1.crud.dealer_crud import crud_dealer
from src.api_v1.crud.order_crud import crud_order

router = APIRouter(prefix='/api/v1', tags=['api_v1'])


@router.post('/add_product/', response_model=ProductRead)
async def add_product(product: ProductCreate,
                      session: Annotated[AsyncSession, Depends(get_async_session)]):
    product = await crud_product.create_product(session=session, product=product)
    return product


@router.post('/add_dealer/', response_model=DealerRead)
async def add_dealer(dealer: DealerCreate,
                     session: Annotated[AsyncSession, Depends(get_async_session)]):
    dealer = await crud_dealer.create_new_dealer(session=session, new_dealer=dealer)
    return dealer


@router.post('/create_order/')
async def create_order(order: OrderCreate,
                       session: Annotated[AsyncSession, Depends(get_async_session)]):
    dealer = await crud_dealer.get_dealer_by_name(session=session,
                                                  dealer_name=order.dealer.name)
    if not dealer:
        dealer = await crud_dealer.create_new_dealer(session=session,
                                                     new_dealer=order.dealer)

    order = await crud_order.create_order(session=session,
                                          dealer_id=dealer.id,
                                          status=order.status,
                                          order=order,)
    return order
