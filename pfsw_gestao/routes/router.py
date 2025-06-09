from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from pfsw_gestao.models.models import User
from pfsw_gestao.schemas import UserDB, UserItemUpdate, UserList, UserItem
from pfsw_gestao.schemas import UserOperations, UserPublic
from pfsw_gestao.database import get_session

router = APIRouter()
database = []


@router.get("/user", response_model=UserList)
async def list_user(session: Session = Depends(get_session)):
    """
    Operação de Listagem de todos os usuários da base.
    """
    users = session.query(User).all()
    user_data = [UserPublic(**user.__dict__) for user in users]

    response = UserList(
        status_code=200,
        message="Lista de usuários",
        items=user_data
    )
    return response


@router.post("/user", response_model=UserPublic, status_code=201)
async def create_user(
    user: UserItem,
    session: Session = Depends(get_session)
):
    """
    Operação de criação de usuários na base.
    """
    print(f"Tipo de session: {type(session)}")
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=400, detail="Usuário já existe.")
        elif db_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email já existe.")

    user_db = User(**user.model_dump())

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return UserPublic.from_orm(user_db)


@router.patch("/user/{id}", response_model=UserOperations)
async def update_partial_user(
    id: int,
    user_update: UserItemUpdate,
    session: Session = Depends(get_session)
):
    """
    Operação de update parcial de usuários na base.
    """
    db_user = session.execute(select(User).where(User.id == id))
    user = db_user.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=400, detail="Usuário não existe na base de dados."
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
        if user_update.phone_number is not None:
            user.phone_number = user_update.phone_number
        if user_update.address is not None:
            user.address = user_update.address
        session.commit()
        return {
            "status_code": 200,
            "message": "Usuário Atualizado com sucesso",
            "new_item": user,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/user/{id}", response_model=UserOperations)
async def update_full_user(
    id: int,
    update_user: UserItem,
    session: Session = Depends(get_session)
):
    """
    Operação de update total de usuários na base.
    """
    db_user = session.execute(select(User).where(User.id == id))
    user = db_user.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=400, detail="Usuário não existe na base de dados."
        )

    user_with_id = UserDB(**update_user.model_dump(), id=id)
    database.append(user_with_id)
    session.commit()
    return {
        "status_code": 200,
        "message": "Usuário Atualizado com sucesso",
        "new_item": user_with_id,
    }


@router.delete("/user/{id}")
async def delete_user(
    id: int = Path(),
    session: Session = Depends(get_session)
):
    """
    Operação de delete de usuários na base.
    """
    db_user = session.execute(select(User).where(User.id == id))
    user = db_user.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=400, detail="Usuário não existe na base de dados."
        )

    session.delete(user)
    session.commit()

    return {"status_code": 200, "message": "Usuário Deletado com sucesso"}
