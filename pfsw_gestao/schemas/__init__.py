from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator
from pydantic.dataclasses import dataclass
from typing import List, Optional


class UserItem(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone_number: Optional[int] = 0
    address: Optional[str] = None
    created_at: Optional[datetime] = datetime.utcnow()


class UserDB(UserItem):
    id: int


@dataclass
class UserItemUpdate:
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone_number: Optional[int] = 0
    address: Optional[str] = None


@field_validator("phone_number", mode="before")
def set_default_phone_number(cls, v):
    return v if v is not None else 0  # Retorna 0 se o valor for None


@dataclass
class UserPublic:
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[int] = None
    created_at: Optional[datetime] = datetime.utcnow()


@dataclass
class UserOperations:
    status_code: int
    message: str
    new_item: UserItem


@dataclass
class UserList:
    status_code: int
    message: str
    items: List[UserPublic]
