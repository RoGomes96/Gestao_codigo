import pytest
from fastapi.testclient import TestClient

from webserver import app


@pytest.fixture
def client():
    return TestClient(app)
