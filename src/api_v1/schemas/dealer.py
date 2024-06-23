from pydantic import BaseModel, EmailStr


class DealerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str


class DealerCreate(DealerBase):
    pass


class DealerRead(DealerBase):
    id: int
