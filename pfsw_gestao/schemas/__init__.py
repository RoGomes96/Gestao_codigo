from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, field_validator
from pydantic.dataclasses import dataclass

from pfsw_gestao.models.models import TodoState


class UserItem(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = "0"
    address: Optional[str] = None


class UserItemFullUpdate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = "0"
    address: Optional[str] = None


class UserDB(UserItem):
    id: int


@dataclass
class UserItemUpdate:
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone_number: Optional[str] = "0"
    address: Optional[str] = None


class UserPublic(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = "0"
    created_at: Optional[datetime] = datetime.utcnow()

    class Config:
        from_attributes = True


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


@dataclass
class Token:
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]


class FilterTodo(FilterPage):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class Message(BaseModel):
    message: str
