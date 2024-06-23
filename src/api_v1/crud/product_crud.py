from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from base_crud import CRUD
from src.models import Product
from src.api_v1.schemas.product import ProductBase, ProductRead, ProductCreate


class CRUDProduct(CRUD):
    async def create_product(self, session: AsyncSession, product: ProductBase) -> ProductRead:
        new_product = self.model(
            name=product.name,
            price=product.price,
        )
        session.add(new_product)
        await session.commit()
        return new_product


crud_product = CRUDProduct(Product)
