from sqlalchemy.orm import Session


class TestUpdatePartialUserEndpoint:
    def test_update_partial_user_sucess(self, client, user, token, session: Session):
        # Arrange
        user_update_data = {"phone_number": 11123456789, "address": "Rua Teste 2"}
        # Act
        response = client.patch(
            f"/user/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json=user_update_data,
        )
        # Assert
        assert response.json()["new_item"]["phone_number"] == 11123456789
        assert response.json()["new_item"]["address"] == "Rua Teste 2"
        assert response.json()["message"] == "Usuário Atualizado com sucesso"

    def test_update_partial_user_fail(self, client, user, token, session: Session):
        # Arrange
        user_update_data = {"phone_number": 11123456789, "address": "Rua Teste Update"}

        # Act
        response = client.patch(
            "/user/2",
            headers={"Authorization": f"Bearer {token}"},
            json=user_update_data,
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Usuário não existe na base de dados."
