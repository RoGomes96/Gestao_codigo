from sqlalchemy.orm import Session


class TestDeleteUserEndpoint:
    def test_delete_user_sucess(self, client, user, token, session: Session):
        # Act
        response = client.delete(
            "/user/1",
            headers={"Authorization": f"Bearer {token}"},
        )
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "Usuário Deletado com sucesso"

    def test_delete_user_fail(self, client, user, token, session: Session):
        # Act
        response = client.delete(
            "/user/2", headers={"Authorization": f"Bearer {token}"}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Usuário não existe na base de dados."
