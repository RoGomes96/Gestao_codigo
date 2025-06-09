from sqlalchemy.orm import Session


class TestListUserEndpoint:
    def test_list_users(self, client, session: Session):
        # Arrange
        user_data = {
            "username": "RodrigoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "rodrigogomes@example.com",
            "password": "password@example",
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
