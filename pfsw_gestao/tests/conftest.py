from contextlib import contextmanager
from datetime import datetime
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, event
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from pfsw_gestao.database import get_session
from pfsw_gestao.models import table_registry
from pfsw_gestao.models.models import User
from pfsw_gestao.security import get_password_hash
from webserver import app


@pytest_asyncio.fixture
async def user(session):
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
    await session.commit()
    await session.refresh(user)

    user.clean_password = user.password

    return user


# Testes
@pytest.fixture(scope="module")
async def test_db():
    # Configuração do banco de dados para testes
    engine = await create_engine(
        'sqlite+aiosqlite:///:memory:', connect_args={"check_same_thread": False}
    )
    # Usando SQLite em memória
    table_registry.metadata.create_all(engine)  # Cria as tabelas
    yield engine
    table_registry.metadata.drop_all(engine)  # Limpa ao final do teste


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


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


@pytest_asyncio.fixture
async def token(client, user):
    response = client.post(
        f"/auth/token/{user.id}",
        data={"username": user.email, "password": "password@example"},
    )
    if response.status_code != HTTPStatus.OK:
        raise ValueError(
            f"Token request failed: {response.status_code}, {response.text}"
        )
    return response.json().get("access_token", None)
