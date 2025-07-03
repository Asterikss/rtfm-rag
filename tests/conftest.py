from fastapi.testclient import TestClient
import pytest

from src.main import app


client = TestClient(app)


@pytest.fixture()
def get_client():
  return client


@pytest.fixture(autouse=True)
def clear_overrides():
  app.dependency_overrides.clear()
  yield
  app.dependency_overrides.clear()
