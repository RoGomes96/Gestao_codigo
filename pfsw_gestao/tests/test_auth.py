from http import HTTPStatus

from sqlalchemy.orm import Session


class TestAuth:

    @staticmethod
    def test_get_token(
        client,
        user,
        token,
        session: Session
    ):
        response = client.post(
            f"/auth/token/{user.id}",
            data={"username": user.email, "password": "password@example"},
        )
        token = response.json()

        assert response.status_code == HTTPStatus.OK
        assert "access_token" in token
        assert "token_type" in token
