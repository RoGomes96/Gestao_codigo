from sqlalchemy.orm import Session


class TestUpdatePartialUserEndpoint:
    def test_update_partial_user_sucess(self, client, session: Session):
        # Arrange
        user_data = {
            "username": "RodrigoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "rodrigogomes@example.com",
            "password": "password@example",
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

    def test_update_partial_user_fail(self, client, session: Session):
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
