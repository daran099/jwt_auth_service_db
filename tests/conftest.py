import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from main import app
from db.base import Base
from core.dependencies import get_db

TEST_DATABASE_URL = "postgresql+psycopg://postgres:277353@localhost:5432/test_db"

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()
