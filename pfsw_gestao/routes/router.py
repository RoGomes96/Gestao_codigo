from fastapi import APIRouter, HTTPException, Path
from pfsw_gestao.schemas import UserDB, UserList, UserItem
from pfsw_gestao.schemas import UserOperations, UserPublic
from pydantic import TypeAdapter

router = APIRouter()
database = []


@router.get("/user", response_model=UserList)
async def list_user():
    """
    Operação de Listagem de todos os usuários da base.
    """
    user = UserItem(username="Rodrigo ",
                    first_name="Rodrigo", last_name="Gomes")
    response = UserList(
        status_code=200, message="Lista de usuários", items=[user])
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
async def update_partial_user(id: int = Path()):
    """
    Operação de update parcial de usuários na base.
    """
    return {"status_code": 200, "message": "Usuário Atualizado com sucesso"}


@router.put("/user/{id}", response_model=UserOperations)
async def update_full_user(id: int = Path()):
    """
    Operação de update total de usuários na base.
    """
    return {"status_code": 200, "message": "Usuário Atualizado com sucesso"}


@router.delete("/user/{id}", response_model=UserOperations)
async def delete_user(id: int = Path()):
    """
    Operação de delete de usuários na base.
    """
    return {"status_code": 200, "message": "Usuário Deletado com sucesso"}
