from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)
