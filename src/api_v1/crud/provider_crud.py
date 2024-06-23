from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.models import Provider
from src.api_v1.crud.base_crud import CRUD
from src.api_v1.schemas.provider import ProviderRead


class ProviderCRUD(CRUD):
    async def get_provider_by_name(self, name: str, session: AsyncSession) -> ProviderRead:
        provider = await session.execute(select(self.model).where(self.model.name == name))
        provider = provider.scalars().first()
        return provider


crud_provider = ProviderCRUD(Provider)
