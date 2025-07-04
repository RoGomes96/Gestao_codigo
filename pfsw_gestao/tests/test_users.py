from http import HTTPStatus

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from pfsw_gestao.models.models import User
from pfsw_gestao.security import verify_password

PHONE_NUMBER_TEST = "11123456789"


class TestUsersEndpoint:

    @staticmethod
    def test_create_user_success(client, session: Session):
        # Arrange
        user_data = {
            "username": "RodrigoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "rodrigogomes@example.com",
            "password": "password@example",
        }

        # Act
        response = client.post("/users/", json=user_data)
        # Assert
        assert response.status_code == HTTPStatus.CREATED
        assert response.json()["username"] == user_data["username"]
        assert response.json()["first_name"] == user_data["first_name"]
        assert response.json()["last_name"] == user_data["last_name"]
        assert response.json()["email"] == user_data["email"]
        assert response.json()["phone_number"] == "0"

    @staticmethod
    def test_create_user_fail(client, session: Session):
        # Arrange
        user_data = {
            "username": "RodrigoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "rodrigogomes@example.com",
            "password": "password@example",
        }
        client.post("/users/", json=user_data)

        # Act
        response = client.post("/users/", json=user_data)

        # Assert
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["detail"] == "Usuário já existe."

    @pytest.mark.asyncio
    async def test_delete_user_sucess(
        self,
        client,
        user,
        token,
        session: Session
    ):
        # Act
        response = client.delete(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        # Assert
        assert response.status_code == HTTPStatus.OK
        assert response.json()["message"] == "Usuário Deletado com sucesso"

    @pytest.mark.asyncio
    async def test_delete_user_fail(
        self,
        client,
        user,
        token,
        session: Session
    ):
        # Act
        response = client.delete(
            "/users/2", headers={"Authorization": f"Bearer {token}"}
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["detail"] == (
            "Usuário não existe na base de dados."
        )

    @staticmethod
    def test_list_users(client, session: Session):
        # Arrange
        user_data = {
            "username": "RodrigoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "rodrigogomes@example.com",
            "password": "password@example",
            "phone_number": "0",
        }

        post_response = client.post("/users/", json=user_data)
        assert post_response.status_code == HTTPStatus.CREATED
        # Act
        response = client.get("/users/")
        created_user = post_response.json()
        created_user_id = created_user["id"]

        # Arrange
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()["items"]) == 1
        assert response.json()["items"][0]["id"] == created_user_id
        assert response.json()["items"][0]["first_name"] == "Rodrigo"
        assert response.json()["items"][0]["last_name"] == "Gomes"
        assert response.json()["items"][0]["email"] == (
            "rodrigogomes@example.com"
        )
        assert response.json()["items"][0]["phone_number"] == "0"

    @staticmethod
    def test_update_partial_user_sucess(client, user, token):
        # Arrange
        user_update_data = {
            "phone_number": PHONE_NUMBER_TEST,
            "address": "Rua Teste 2"
        }
        # Act
        response = client.patch(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json=user_update_data,
        )
        print(response.json())
        # Assert
        assert response.json()["new_item"]["phone_number"] == PHONE_NUMBER_TEST
        assert response.json()["new_item"]["address"] == "Rua Teste 2"
        assert response.json()["message"] == "Usuário Atualizado com sucesso"

    @staticmethod
    def test_update_partial_user_fail(client, token):
        # Arrange
        user_update_data = {
            "phone_number": PHONE_NUMBER_TEST,
            "address": "Rua Teste Update"
        }

        # Act
        response = client.patch(
            "/users/2",
            headers={"Authorization": f"Bearer {token}"},
            json=user_update_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["detail"] == (
            "Usuário não existe na base de dados."
        )

    @pytest.mark.asyncio
    async def test_update_total_user_sucess(
        self,
        client,
        user,
        token,
        session: Session
    ):
        user_update_data = {
            "username": "RoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "Rodrigo@example.com",
            "password": "password2@example",
            "phone_number": PHONE_NUMBER_TEST,
            "address": "Rua Teste Update",
        }
        # Act
        response = client.put(
            f"/users/{user.id}",  # Verifique se o ID está correto
            headers={"Authorization": f"Bearer {token}"},
            json=user_update_data,
        )
        result = await session.execute(
            select(User).where(User.id == user.id)
        )
        updated_user = result.scalar_one_or_none()
        # Assert
        assert verify_password(
            user_update_data["password"],
            updated_user.password
        )
        assert response.json()["new_item"]["username"] == "RoGomes"
        assert response.json()["new_item"]["email"] == "Rodrigo@example.com"
        assert response.json()["new_item"]["phone_number"] == PHONE_NUMBER_TEST
        assert response.json()["new_item"]["address"] == "Rua Teste Update"
        assert response.json()["message"] == "Usuário Atualizado com sucesso"

    @staticmethod
    def test_update_total_user_fail(client, token):
        # Arrange
        user_update_data = {
            "username": "RoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "Gomes@example.com",
            "password": "password@example2",
            "phone_number": PHONE_NUMBER_TEST,
            "address": "Rua Teste Update",
        }

        # Act
        response = client.put(
            "/users/2",
            headers={"Authorization": f"Bearer {token}"},
            json=user_update_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["detail"] == (
            "Usuário não existe na base de dados."
        )

    @staticmethod
    def test_update_total_user_bad_request(client, token):
        # Arrange
        user_update_data = {
            "username": "RoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "phone_number": PHONE_NUMBER_TEST,
            "address": "Rua Teste Update",
        }

        # Act
        response = client.put(
            "/users/1",
            headers={"Authorization": f"Bearer {token}"},
            json=user_update_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    def test_update_user_with_wrong_user(self, client, other_user, token):
        # Arrange
        user_update_data = {
            "username": "RoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "Gomes@example.com",
            "password": "password@example2",
            "phone_number": PHONE_NUMBER_TEST,
            "address": "Rua Teste Update",
        }

        response = client.put(
            f'/users/{other_user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json=user_update_data,
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == {
            'detail': 'Usuário sem permissão suficiente.'
        }

    def test_delete_user_wrong_user(self, client, other_user, token):
        response = client.delete(
            f'/users/{other_user.id}',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == {
            'detail': 'Usuário sem permissão suficiente.'
        }
