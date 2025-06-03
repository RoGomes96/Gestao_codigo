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
    adress: Optional[str] = None


@field_validator('phone_number', mode='before')
def set_default_phone_number(cls, v):
    return v if v is not None else 0  # Retorna 0 se o valor for None


@dataclass
class UserList:
    status_code: int
    message: str
    items: List[UserItem]


@dataclass
class UserOperations:
    status_code: int
    message: str


@dataclass
class UserPublic:
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[int] = None


class UserDB(UserItem):
    id: int
