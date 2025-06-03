import pytest
from fastapi.testclient import TestClient
from webserver import app

client = TestClient(app)


class TestCreateUserEndpoint:
    def setup_method(self):
        global database
        database = []

    def test_list_users(self):
        # Arrange
        user_data = {
            "username": "RodrigoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "rodrigogomes@example.com",
            "phone_number": 0,
        }

        client.post("/user", json=user_data)

        # Act
        response = client.get("/user")

        # Arrange
        assert response.status_code == 200
        assert len(response.json()["items"]) == 1
        assert response.json()["items"][0]["id"] == 1
        assert response.json()["items"][0]["first_name"] == "Rodrigo"
        assert response.json()["items"][0]["last_name"] == "Gomes"
        assert response.json()["items"][0]["email"] == "rodrigogomes@example.com"
        assert response.json()["items"][0]["phone_number"] == 0
