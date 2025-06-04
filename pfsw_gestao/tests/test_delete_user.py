import pytest
from fastapi.testclient import TestClient
from webserver import app

client = TestClient(app)


class TestDeleteUserEndpoint:
    def setup_method(self):
        global database
        database = []

    def test_delete_user_sucess(self):

        # Arrange
        user_data = {
            "username": "RodrigoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "rodrigogomes@example.com",
            "password": "password@example",
            "phone_number": 1234
        }

        client.post("/user", json=user_data)

        # Act
        response = client.delete("/user/1")

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "Usuário Deletado com sucesso"

    def test_delete_user_fail(self):

        # Act
        response = client.delete("/user/1")

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Usuário não existe na base de dados."
