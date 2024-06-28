from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.models import Provider
from src.api_v1.crud.base_crud import CRUD
from src.api_v1.schemas import ProviderRead, ProviderCreate


class ProviderCRUD(CRUD):
    async def create_provider(self, session: AsyncSession, provider: ProviderCreate) -> ProviderRead:
        provider = self.model(**provider.dict())
        session.add(provider)
        await session.commit()
        return provider

    async def get_provider_by_name(self, name: str, session: AsyncSession) -> ProviderRead:
        provider = await session.execute(select(self.model).where(self.model.name == name))
        provider = provider.scalars().first()
        return provider

    async def get_all_providers(self, session: AsyncSession) -> list[ProviderRead]:
        providers = await session.execute(select(self.model).order_by(self.model.name))
        providers = providers.scalars().all()
        return [ProviderRead(id=provider.id, name=provider.name, email=provider.email, phone=provider.phone)
                for provider in providers]


crud_provider = ProviderCRUD(Provider)
