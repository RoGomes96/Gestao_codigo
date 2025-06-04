from fastapi import APIRouter, HTTPException, Path
from pfsw_gestao.schemas import UserDB, UserItemUpdate, UserList, UserItem
from pfsw_gestao.schemas import UserOperations, UserPublic
from pydantic import EmailStr, TypeAdapter

router = APIRouter()
database = []


@router.get("/user", response_model=UserList)
async def list_user():
    """
    Operação de Listagem de todos os usuários da base.
    """
    user = [UserPublic(**user.__dict__) for user in database]
    response = UserList(status_code=200, message="Lista de usuários", items=user)
    return TypeAdapter(UserList).dump_python(response, by_alias=True)


@router.post("/user", response_model=UserPublic, status_code=201)
async def create_user(user: UserItem):
    """
    Operação de criação de usuários na base.
    """
    for existing_user in database:
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Usuário já existe.")
    user_validated = UserItem(**user.model_dump())
    user_with_id = UserDB(**user_validated.model_dump(), id=len(database) + 1)
    user_public = UserPublic(**user_with_id.model_dump())

    database.append(user_with_id)

    return user_public


@router.patch("/user/{id}", response_model=UserOperations)
async def update_partial_user(id: int, user_update: UserItemUpdate):
    """
    Operação de update parcial de usuários na base.
    """
    existing_user = None
    for user in database:
        if user.id == id:
            existing_user = user
            break
    if existing_user is None:
        raise HTTPException(
            status_code=400, detail="Usuário não existe na base de dados."
        )

    try:
        if user_update.username is not None:
            existing_user.username = user_update.username
        if user_update.first_name is not None:
            existing_user.first_name = user_update.first_name
        if user_update.last_name is not None:
            existing_user.last_name = user_update.last_name
        if user_update.email is not None:
            existing_user.email = user_update.email
        if user_update.phone_number is not None:
            existing_user.phone_number = user_update.phone_number
        if user_update.address is not None:
            existing_user.address = user_update.address

        return {
            "status_code": 200,
            "message": "Usuário Atualizado com sucesso",
            "new_item": existing_user,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/user/{id}", response_model=UserOperations)
async def update_full_user(id: int, update_user: UserItem):
    """
    Operação de update total de usuários na base.
    """
    existing_user = None
    for user in database:
        if user.id == id:
            existing_user = user
            database.remove(user)
            break
    if existing_user is None:
        raise HTTPException(
            status_code=400, detail="Usuário não existe na base de dados."
        )

    user_with_id = UserDB(**update_user.model_dump(), id=id)
    database.append(user_with_id)
    return {
        "status_code": 200,
        "message": "Usuário Atualizado com sucesso",
        "new_item": user_with_id,
    }


@router.delete("/user/{id}")
async def delete_user(id: int = Path()):
    """
    Operação de delete de usuários na base.
    """
    existing_user = None
    for user in database:
        if user.id == id:
            database.remove(user)
            existing_user = True
            break
    if existing_user is None:
        raise HTTPException(
            status_code=400, detail="Usuário não existe na base de dados."
        )
    return {"status_code": 200, "message": "Usuário Deletado com sucesso"}
