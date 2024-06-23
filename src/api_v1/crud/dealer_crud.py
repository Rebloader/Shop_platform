from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.crud.base_crud import CRUD
from src.api_v1.schemas.dealer import DealerCreate, DealerRead
from src.models import Dealer


class CRUDDealer(CRUD):
    async def create_new_dealer(self, session: AsyncSession, new_dealer: DealerCreate) -> DealerRead:
        new_dealer = self.model(
            name=new_dealer.name,
            email=new_dealer.email,
            phone=new_dealer.phone,
            address=new_dealer.address,
        )
        session.add(new_dealer)
        await session.commit()
        return new_dealer

    async def update_dealer(self):
        pass

    async def delete_dealer(self):
        pass


crud_dealer = CRUDDealer(Dealer)
