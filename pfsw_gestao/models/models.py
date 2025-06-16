from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, Integer, String, func
from enum import Enum
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from pfsw_gestao.models.base import Base


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )
    password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[Optional[BigInteger]] = mapped_column(
        String,
        nullable=True
    )
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(

        server_default=func.now()
    )
    todos: Mapped[list['Todo']] = relationship(

        cascade='all, delete-orphan',
        lazy='selectin',
    )


class Todo(Base):
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState] = mapped_column(String, nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id')
    )
