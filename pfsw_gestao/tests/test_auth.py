from http import HTTPStatus
import pytest

from sqlalchemy.orm import Session


class TestAuth:

    @pytest.mark.asyncio
    async def test_get_token(
        self,
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
