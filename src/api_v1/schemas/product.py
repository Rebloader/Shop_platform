from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int
    price: int
