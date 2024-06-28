from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.crud.base_crud import CRUD
from src.api_v1.schemas.dealer import DealerCreate, DealerRead
from src.models import Dealer


class DealerCRUD(CRUD):
    async def create_new_dealer(self, session: AsyncSession, new_dealer: DealerCreate) -> DealerRead:
        new_dealer = self.model(
            name=new_dealer.name,
            email=new_dealer.email,
            phone=new_dealer.phone,
            address=new_dealer.address,
        )
        session.add(new_dealer)
        await session.commit()
        await session.refresh(new_dealer)
        return new_dealer

    async def get_dealer_by_name(self, session: AsyncSession, dealer_name: str) -> DealerRead:
        dealer = await session.execute(select(self.model).where(self.model.name == dealer_name))
        dealer = dealer.scalars().first()
        return dealer

    async def get_dealer_list(self, session: AsyncSession) -> list[DealerRead]:
        dealer_list = await session.execute(select(self.model).order_by(self.model.id))
        dealer_list = dealer_list.scalars().all()
        return [DealerRead(id=dealer.id, name=dealer.name, email=dealer.email,
                           phone=dealer.phone, address=dealer.address) for dealer in dealer_list]

    async def update_dealer(self):
        pass

    async def delete_dealer(self):
        pass


crud_dealer = DealerCRUD(Dealer)
