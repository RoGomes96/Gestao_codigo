from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import ForeignKey, Integer, String, func
from enum import Enum
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    registry,
    relationship
)

table_registry = registry()


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[EmailStr] = mapped_column(
        String,
        nullable=False,
        unique=True
    )
    password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now()
    )
    todos: Mapped[list['Todo']] = relationship( 
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )


@table_registry.mapped_as_dataclass
class Todo:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState] 

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id')
    ) 
