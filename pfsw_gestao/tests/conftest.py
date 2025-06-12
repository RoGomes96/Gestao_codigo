from contextlib import contextmanager
from datetime import datetime
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from pfsw_gestao.database import get_session
from pfsw_gestao.models import table_registry
from pfsw_gestao.models.models import User
from pfsw_gestao.security import get_password_hash
from webserver import app


@pytest.fixture
def user(session):
    user = User(
        username="RodrigoGomes",
        first_name="Rodrigo",
        last_name="Gomes",
        email="Rodrigo@example.com",
        password=get_password_hash("password@example"),
        phone_number=1234567890,
        address="Rua Teste",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = user.password

    return user


# Testes
@pytest.fixture(scope="module")
def test_db():
    # Configuração do banco de dados para testes
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    # Usando SQLite em memória
    table_registry.metadata.create_all(engine)  # Cria as tabelas
    yield engine
    table_registry.metadata.drop_all(engine)  # Limpa ao final do teste


@pytest.fixture
def session(test_db):
    """Cria uma nova sessão para cada teste e limpa as tabelas."""
    connection = test_db.connect()
    Session = sessionmaker(bind=connection)
    session = Session()

    session.query(User).delete()
    session.commit()
    session.commit()

    yield session

    session.close()
    connection.close()


@pytest.fixture
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_session] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 6, 5)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time

    event.listen(model, "before_insert", fake_time_hook)

    yield time

    event.remove(model, "before_insert", fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def token(client, user):
    response = client.post(
        f"/auth/token/{user.id}",
        data={"username": user.email, "password": "password@example"},
    )
    if response.status_code != HTTPStatus.OK:
        raise ValueError(
            f"Token request failed: {response.status_code}, {response.text}"
        )
    return response.json().get("access_token", None)
