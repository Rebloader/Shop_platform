from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_helper import get_async_session

from src.api_v1.schemas import ProviderCreate, ProviderRead
from src.api_v1.crud.provider_crud import crud_provider

router = APIRouter(prefix='/provider', tags=['Providers'])


@router.get('/all/', response_model=list[ProviderRead])
async def get_provider_list(session: Annotated[AsyncSession, Depends(get_async_session)]):
    providers = await crud_provider.get_all_providers(session=session)
    return providers


@router.post('/create/', response_model=ProviderRead)
async def add_provider(provider: ProviderCreate,
                       session: Annotated[AsyncSession, Depends(get_async_session)]):
    provider = await crud_provider.create_provider(session=session, provider=provider)
    return provider
