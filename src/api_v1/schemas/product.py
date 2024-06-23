from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: int


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int
