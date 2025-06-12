from dataclasses import asdict
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.orm import Session

from pfsw_gestao.models import User


class TestUserDB:
    def test_create_user(self, session, mock_db_time):
        # Arrange
        with mock_db_time(model=User) as time:
            new_user = User(
                username="RodrigoGomes",
                first_name="Rodrigo",
                last_name="Gomes",
                email="rodrigogomes@example.com",
                password="password@example",
                phone_number=0,
                address="",
            )

            session.add(new_user)
            session.commit()

        # act
        user = session.scalar(select(User).where(User.username == "RodrigoGomes"))

        # Assert
        assert user is not None
        assert asdict(user) == {
            "id": 1,
            "username": "RodrigoGomes",
            "first_name": "Rodrigo",
            "last_name": "Gomes",
            "password": "password@example",
            "email": "rodrigogomes@example.com",
            "phone_number": 0,
            "address": "",
            "created_at": time,
        }

    def test_get_token(self, client, user, token, session: Session):
        response = client.post(
            f"/token/{user.id}",
            data={"username": user.email, "password": "password@example"},
        )
        token = response.json()

        assert response.status_code == HTTPStatus.OK
        assert "access_token" in token
        assert "token_type" in token
