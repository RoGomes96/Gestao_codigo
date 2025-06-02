from fastapi import APIRouter, Path
from schemas import UserList, UserItem, UserOperations
from pydantic import TypeAdapter

router = APIRouter()


@router.get("/user", response_model=UserList)
async def list_user():

    user = UserItem(username="Rodrigo ", first_name="Rodrigo", last_name="Gomes")
    response = UserList(status_code=200, message="Lista de usuários", items=[user])
    return TypeAdapter(UserList).dump_python(response, by_alias=True)


@router.post("/user")
async def create_user():
    return {"status_code": 200, "message": "Usuário Criado com sucesso"}


@router.patch("/user/{id}", response_model=UserOperations)
async def update_partial_user(id: int = Path()):
    return {"status_code": 200, "message": "Usuário Atualizado com sucesso"}


@router.put("/user/{id}", response_model=UserOperations)
async def update_full_user(id: int = Path()):
    return {"status_code": 200, "message": "Usuário Atualizado com sucesso"}


@router.delete("/user/{id}", response_model=UserOperations)
async def delete_user(id: int = Path()):
    return {"status_code": 200, "message": "Usuário Deletado com sucesso"}
