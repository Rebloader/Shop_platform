from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.crud.dealer_crud import crud_dealer
from src.db_helper import get_async_session
from src.tasks.celery_task import send_email_to_dealer

router = APIRouter(prefix='/messages', tags=['messages'])


@router.get('/send_email_order_info/')
async def send_message_to_email(dealer_name: str,
                                session: Annotated[AsyncSession, Depends(get_async_session)],
                                file_name: str):
    dealer = await crud_dealer.get_dealer_by_name(session=session, dealer_name=dealer_name)
    if not dealer:
        raise HTTPException(status_code=404, detail='Dealer not found')
    dealer_email = dealer.email

    task = send_email_to_dealer.delay(dealer_email=dealer_email, file_name=file_name)

    return {'status': 'success', 'message': 'Email sent successfully', 'task_id': task.id}
