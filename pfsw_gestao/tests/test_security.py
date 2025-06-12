from sqlalchemy.orm import Session
from jwt import decode

from pfsw_gestao.security import SECRET_KEY, create_access_token


def test_jwt():
    data = {"test": "test"}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=["HS256"])

    assert decoded["test"] == data["test"]
    assert "exp" in decoded


def test_jwt_invalid_token(client, user, session: Session):
    response = client.delete(
        "/user/1",
        headers={"Authorization": "Bearer token"},
    )
    print(response.json())

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
