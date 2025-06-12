from sqlalchemy.orm import Session

from pfsw_gestao.models.models import User
from pfsw_gestao.security import verify_password


class TestUpdateTotalUserEndpoint:
    def test_update_total_user_sucess(self, client, user, token, session: Session):
        user_update_data = {
            "username": "RoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "Rodrigo@example.com",
            "password": "password2@example",
            "phone_number": 11123456789,
            "address": "Rua Teste Update",
        }
        # Act
        response = client.put(
            f"/user/{user.id}",  # Verifique se o ID está correto
            headers={"Authorization": f"Bearer {token}"},
            json=user_update_data,
        )
        updated_user = session.query(User).filter_by(id=user.id).first()
        # Assert
        assert verify_password(user_update_data["password"], updated_user.password)
        assert response.json()["new_item"]["username"] == "RoGomes"
        assert response.json()["new_item"]["email"] == "Rodrigo@example.com"
        assert response.json()["new_item"]["phone_number"] == 11123456789
        assert response.json()["new_item"]["address"] == "Rua Teste Update"
        assert response.json()["message"] == "Usuário Atualizado com sucesso"

    def test_update_total_user_fail(self, client, user, token, session: Session):
        # Arrange
        user_update_data = {
            "username": "RoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "email": "Gomes@example.com",
            "password": "password@example2",
            "phone_number": 11123456789,
            "address": "Rua Teste Update",
        }

        # Act
        response = client.put(
            "/user/2",
            headers={"Authorization": f"Bearer {token}"},
            json=user_update_data,
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Usuário não existe na base de dados."

    def test_update_total_user_bad_request(self, client, user, token, session: Session):
        # Arrange
        user_update_data = {
            "username": "RoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "phone_number": 11123456789,
            "address": "Rua Teste Update",
        }

        # Act
        response = client.put(
            "/user/1",
            headers={"Authorization": f"Bearer {token}"},
            json=user_update_data,
        )

        # Assert
        assert response.status_code == 422
