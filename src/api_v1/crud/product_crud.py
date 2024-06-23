from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.crud.base_crud import CRUD
from src.api_v1.schemas.product import ProductRead, ProductCreate
from src.models import Product


class CRUDProduct(CRUD):
    async def create_product(self, session: AsyncSession, product: ProductCreate) -> ProductRead:
        new_product = self.model(
            name=product.name,
            price=product.price,
        )
        session.add(new_product)
        await session.commit()
        return new_product


crud_product = CRUDProduct(Product)
