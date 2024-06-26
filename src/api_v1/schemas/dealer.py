from pydantic import BaseModel, EmailStr, Field


class DealerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=11)
    address: str


class DealerCreate(DealerBase):
    pass


class DealerRead(DealerBase):
    id: int
