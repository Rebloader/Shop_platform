from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUD:
    def __init__(self, model):
        self.model = model

    async def get_all_items(self, session: AsyncSession):
        items = await session.execute(select(self.model).order_by(self.model.id))
        return items.scalars().all()

    async def get_item_by_id(self, id_: int, session: AsyncSession):
        item = await session.get(self.model, id_)
        return item
