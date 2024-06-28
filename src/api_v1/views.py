from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_helper import get_async_session

from src.api_v1.crud.order_crud import crud_order
from src.utils.convert_files.base_serializer import serialized_for_output
from src.utils.convert_files.converter_to_excel import create_excel_file_with_order_info


router = APIRouter(prefix='/api/v1', tags=['api_v1'])


@router.get('/get_serializer_file/')
async def get_serializer_file(order_id: int, session: Annotated[AsyncSession, Depends(get_async_session)]):
    order = await crud_order.get_order_by_id(session=session, order_id=order_id)
    dict_to_msg = await serialized_for_output(order=order)
    file_path = await create_excel_file_with_order_info(dict_to_msg)
    return {'dict': dict_to_msg, 'file_path': file_path}

