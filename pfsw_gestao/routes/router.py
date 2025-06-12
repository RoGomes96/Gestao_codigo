from http import HTTPStatus
from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from pfsw_gestao.models.models import User
from pfsw_gestao.schemas import (
    Token,
    UserItemFullUpdate,
    UserItemUpdate,
    UserList,
    UserItem,
)
from pfsw_gestao.schemas import UserOperations, UserPublic
from pfsw_gestao.database import get_session
from pfsw_gestao.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

router = APIRouter()
database = []


@router.post("/token/{id}", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user", response_model=UserList)
async def list_user(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    """
    Operação de Listagem de todos os usuários da base.
    """
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    user_data = [UserPublic(**user.__dict__) for user in users]

    response = UserList(
        status_code=200,
        message="Lista de usuários",
        items=user_data
    )
    return response


@router.post("/user", response_model=UserPublic, status_code=201)
async def create_user(user: UserItem, session: Session = Depends(get_session)):
    """
    Operação de criação de usuários na base.
    """
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
    session.commit()
    session.refresh(user_db)

    return UserPublic.from_orm(user_db)


@router.patch("/user/{id}", response_model=UserOperations)
async def update_partial_user(
    id: int,
    user_update: UserItemUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
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
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
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
        session.commit()
        session.refresh(user)
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
    update_user: UserItemFullUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
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
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
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
        session.commit()
        session.refresh(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status_code": 200,
        "message": "Usuário Atualizado com sucesso",
        "new_item": user,
    }


@router.delete("/user/{id}")
async def delete_user(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Operação de delete de usuários na base.
    """
    db_user = session.execute(select(User).where(User.id == id))
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

    session.delete(user)
    session.commit()

    return {"status_code": 200, "message": "Usuário Deletado com sucesso"}
