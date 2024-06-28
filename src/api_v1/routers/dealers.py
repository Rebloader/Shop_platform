from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_helper import get_async_session

from src.api_v1.schemas import OrderRead, DealerRead
from src.api_v1.crud.order_crud import crud_order
from src.api_v1.crud.dealer_crud import crud_dealer

router = APIRouter(prefix='/dealer', tags=["Dealers"])


@router.get('/all/', response_model=list[DealerRead])
async def get_all_dealers(session: Annotated[AsyncSession, Depends(get_async_session)]):
    dealers = await crud_dealer.get_dealer_list(session=session)
    return dealers


@router.get('/orders/', response_model=list[OrderRead])
async def get_dealer_orders_by_id(session: Annotated[AsyncSession, Depends(get_async_session)],
                                  dealer_name: str):
    dealer = await crud_dealer.get_dealer_by_name(session=session, dealer_name=dealer_name)
    if not dealer:
        raise HTTPException(404, 'Dealer not found')
    result = await crud_order.get_dealer_orders(session=session, dealer_id=dealer.id)
    return result
