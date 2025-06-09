from sqlalchemy.orm import Session


class TestCreateUserEndpoint:
    def test_create_user_success(self, client, session: Session):
        # Arrange
        user_data = {
            "username": "RodrigoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "rodrigogomes@example.com",
            "password": "password@example"
        }

        # Act
        response = client.post("/user", json=user_data)

        # Assert
        assert response.status_code == 201
        assert response.json()["username"] == user_data["username"]
        assert response.json()["first_name"] == user_data["first_name"]
        assert response.json()["last_name"] == user_data["last_name"]
        assert response.json()["email"] == user_data["email"]
        assert response.json()["phone_number"] == 0

    def test_create_user_fail(self, client, session: Session):
        # Arrange
        user_data = {
            "username": "RodrigoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "rodrigogomes@example.com",
            "password": "password@example"
        }
        client.post("/user", json=user_data)

        # Act
        response = client.post("/user", json=user_data)

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Usuário já existe."
