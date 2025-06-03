import pytest
from fastapi.testclient import TestClient
from webserver import app

client = TestClient(app)


class TestCreateUserEndpoint:
    def setup_method(self):
        global database
        database = []

    def test_list_users_sucess(self):
        # Arrange
        user_data = {
            "username": "RodrigoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "rodrigogomes@example.com",
            "phone_number": 1234,
        }

        client.post("/user", json=user_data)
        user_update_data = {
            "phone_number": 11123456789,
            "address": "Rua Teste Update"
        }

        # Act
        response = client.patch("/user/1", json=user_update_data)

        # Assert
        assert response.json()["new_item"]["phone_number"] == 11123456789
        assert response.json()["new_item"]["address"] == "Rua Teste Update"
        assert response.json()["message"] == "Usuário Atualizado com sucesso"

    def test_list_users_false(self):
        # Arrange
        user_update_data = {
            "phone_number": 11123456789,
            "address": "Rua Teste Update"
        }

        # Act
        response = client.patch("/user/2", json=user_update_data)

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Usuário não existe na base de dados."
