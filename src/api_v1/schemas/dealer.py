from pydantic import BaseModel, EmailStr, Field


class DealerBase(BaseModel):
    name: str
    email: EmailStr


class DealerCreate(DealerBase):
    phone: str = Field(..., min_length=10, max_length=11, example='88005553535')
    address: str = Field(..., min_length=7, max_length=250, example='г. Москва, ул. Мира, д. 1')


class DealerRead(DealerBase):
    id: int
    phone: str
    address: str
