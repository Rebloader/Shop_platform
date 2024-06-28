from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.crud.base_crud import CRUD
from src.api_v1.schemas import ProductRead, ProductCreate
from src.models import Product


class ProductCRUD(CRUD):
    async def create_product(self, session: AsyncSession, product: ProductCreate) -> ProductRead:
        new_product = self.model(
            name=product.name,
            price=0,
        )
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        return new_product

    async def get_product_by_name(self, session: AsyncSession, product_name: str) -> ProductRead:
        product = await session.execute(select(self.model).where(self.model.name == product_name))
        product = product.scalars().first()
        return product

    async def patch_product_price(self, session: AsyncSession, product_id: int, new_price: int) -> ProductRead:
        updated_product = self.model(
            price=new_price,
        )
        session.add(updated_product)
        await session.commit()
        return updated_product


crud_product = ProductCRUD(Product)
