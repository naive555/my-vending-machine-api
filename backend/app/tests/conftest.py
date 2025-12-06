import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, get_db
from app.core.test_database import engine_test, TestingSessionLocal


@pytest.fixture(scope="function")
def db():
    """
    Provides a SQLAlchemy session for a test.
    Uses a transaction rollback to reset DB after each test.
    """
    connection = engine_test.connect()
    transaction = connection.begin()

    # Use a session bound to the connection
    Base.metadata.create_all(bind=engine_test)
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
        Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="function")
def client(db):
    """
    Provides a FastAPI TestClient that uses the test DB session.
    """

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
