from pydantic import BaseModel, EmailStr


class ProviderBase(BaseModel):
    name: str
    email: EmailStr
    phone: str


class ProviderCreate(ProviderBase):
    pass


class ProviderRead(ProviderBase):
    id: int
