from pydantic import BaseModel, EmailStr, Field


class ProviderBase(BaseModel):
    name: str
    email: EmailStr


class ProviderCreate(ProviderBase):
    phone: str = Field(..., min_length=8, max_length=12, example='88005553535')


class ProviderRead(ProviderBase):
    id: int
    phone: str
