from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pfsw_gestao.database import get_session
from pfsw_gestao.models.models import User
from pfsw_gestao.schemas import (
    FilterPage,
    UserItem,
    UserItemFullUpdate,
    UserItemUpdate,
    UserList,
    UserOperations,
    UserPublic,
)
from pfsw_gestao.security import (
    get_current_user,
    get_password_hash,
)

SessionUser = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/users', tags=['users'])


@router.get("/", response_model=UserList)
async def list_user(
    session: SessionUser,
    filter_users: Annotated[FilterPage, Query()]
):
    """
    Operação de Listagem de todos os usuários da base.
    """
    query = await session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    )
    users = query.all()
    user_data = [UserPublic(**user.__dict__) for user in users]

    response = UserList(
        status_code=200,
        message="Lista de usuários",
        items=user_data
    )
    return response


@router.post("/", response_model=UserPublic, status_code=201)
async def create_user(user: UserItem, session: SessionUser):
    """
    Operação de criação de usuários na base.
    """
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=400, detail="Usuário já existe.")
        elif db_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email já existe.")

    hashed_password = get_password_hash(user.password)

    user_db = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        username=user.username,
        password=hashed_password,
        phone_number=user.phone_number,
        address=user.address,
    )

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)

    return UserPublic.from_orm(user_db)


@router.patch("/{id}", response_model=UserOperations)
async def update_partial_user(
    id: int,
    user_update: UserItemUpdate,
    session: SessionUser,
    current_user: CurrentUser,
):
    """
    Operação de update parcial de usuários na base.
    """
    db_user = await session.execute(select(User).where(User.id == id))
    user = db_user.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=400, detail="Usuário não existe na base de dados."
        )
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Usuário sem permissão suficiente."
        )
    try:
        if user_update.username is not None:
            user.username = user_update.username
        if user_update.first_name is not None:
            user.first_name = user_update.first_name
        if user_update.last_name is not None:
            user.last_name = user_update.last_name
        if user_update.email is not None:
            user.email = user_update.email
        if user_update.password is not None:
            user.password = get_password_hash(user_update.password)
        if user_update.phone_number is not None:
            user.phone_number = user_update.phone_number
        if user_update.address is not None:
            user.address = user_update.address
        await session.commit()
        await session.refresh(user)
        return {
            "status_code": 200,
            "message": "Usuário Atualizado com sucesso",
            "new_item": user,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{id}", response_model=UserOperations)
async def update_full_user(
    id: int,
    update_user: UserItemFullUpdate,
    session: SessionUser,
    current_user: CurrentUser,
):
    """
    Operação de update total de usuários na base.
    """
    db_user = await session.execute(select(User).where(User.id == id))
    user = db_user.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não existe na base de dados.",
        )

    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Usuário sem permissão suficiente."
        )

    user.username = update_user.username
    user.first_name = update_user.first_name
    user.last_name = update_user.last_name
    user.email = update_user.email
    if update_user.password:
        user.password = get_password_hash(update_user.password)
    user.phone_number = update_user.phone_number
    user.address = update_user.address

    try:
        await session.commit()
        await session.refresh(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status_code": 200,
        "message": "Usuário Atualizado com sucesso",
        "new_item": user,
    }


@router.delete("/{id}")
async def delete_user(
    id: int,
    session: SessionUser,
    current_user: CurrentUser,
):
    """
    Operação de delete de usuários na base.
    """
    db_user = await session.execute(select(User).where(User.id == id))
    user = db_user.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não existe na base de dados.",
        )
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Usuário sem permissão suficiente."
        )

    await session.delete(current_user)
    await session.commit()

    return {"status_code": 200, "message": "Usuário Deletado com sucesso"}
