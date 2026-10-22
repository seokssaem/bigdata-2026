import os

os.environ["DATABASE_URL"] = "sqlite:///./test_inventory.db"

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.forecast_service import forecast_service
from app.main import app


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def reset_forecast_cache():
    """예측 서비스는 학습 결과를 메모리에 캐시하므로 테스트마다 비운다."""
    forecast_service._state = None
    yield
    forecast_service._state = None


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

