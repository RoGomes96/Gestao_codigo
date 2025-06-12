from http import HTTPStatus

from jwt import decode

from pfsw_gestao.security import create_access_token, settings


class TestApp:
    @staticmethod
    def test_jwt():
        data = {"test": "test"}
        token = create_access_token(data)

        decoded = decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        assert decoded["test"] == data["test"]
        assert "exp" in decoded

    @staticmethod
    def test_jwt_invalid_token(client):
        response = client.delete(
            "/users/1",
            headers={"Authorization": "Bearer token"},
        )
        print(response.json())

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}
