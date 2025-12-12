from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    role: str = "nurse"


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
