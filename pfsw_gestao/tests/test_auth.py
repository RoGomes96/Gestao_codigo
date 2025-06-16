from http import HTTPStatus
from freezegun import freeze_time
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

    def test_token_expired_after_time(self, client, user):
        user_data = {
            "username": "errado",
            "first_name": "errado",
            "last_name": "errado",
            "email": "errado@example.com",
            "password": "errado@example",
            "phone_number": "0",
            "adress": "Rua errada"
        }
        with freeze_time('2025-06-13 12:00:00'):
            response = client.post(
                f'/auth/token/{user.id}',
                data={'username': user.email, 'password': "password@example"},
            )
            assert response.status_code == HTTPStatus.OK
            token = response.json()['access_token']

        with freeze_time('2025-06-13 12:31:00'):
            response = client.put(
                f'/users/{user.id}',
                headers={'Authorization': f'Bearer {token}'},
                json=user_data,
            )
            assert response.status_code == HTTPStatus.UNAUTHORIZED
            assert response.json() == {
                'detail': 'Não foi possivel verificar as credenciais.'
            }

    def test_token_inexistent_user(self, client):
        response = client.post(
            '/auth/token/3',
            data={'username': 'no_user@no_domain.com', 'password': 'testtest'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Email ou password incorretos.'}

    def test_token_wrong_password(self, client, user):
        response = client.post(
            '/auth/token/1',
            data={'username': user.email, 'password': 'wrong_password'}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Email ou password incorretos.'}

    def test_refresh_token(self, client, token):
        response = client.post(
            '/auth/refresh_token/1',
            headers={'Authorization': f'Bearer {token}'},
        )

        data = response.json()

        assert response.status_code == HTTPStatus.OK
        assert 'access_token' in data
        assert 'token_type' in data
        assert data['token_type'] == 'bearer'

    def test_token_expired_dont_refresh(self, client, user):
        with freeze_time('2023-07-14 12:00:00'):
            response = client.post(
                '/auth/token/1',
                data={'username': user.email, 'password': "password@example"},
            )
            assert response.status_code == HTTPStatus.OK
            token = response.json()['access_token']

        with freeze_time('2023-07-14 12:31:00'):
            response = client.post(
                '/auth/refresh_token/1',
                headers={'Authorization': f'Bearer {token}'},
            )
            assert response.status_code == HTTPStatus.UNAUTHORIZED
            assert response.json() == {
                'detail': 'Não foi possivel verificar as credenciais.'
            }
