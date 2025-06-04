"""
Pytest conftest module for AutoRect

- Loads the test MySQL DB (testautorentdb)
- All API tests use TestClient with overridden get_db dependency (repository/unit tests get a fresh SQLAlchemy session)
- All DB changes are rolled back after each test to keep tests isolated

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
"""

import pytest
from fastapi.testclient import TestClient
import os
from sqlalchemy import text

os.environ["DATABASE_URL"] = "mysql+pymysql://root:1234@localhost:3306/testautorentdb"
from app.db.base import Base
from app.db.session import SessionLocal, engine

# Force-import all models so that Base.metadata sees them
import app.models

from app.main import app

# ------------------------
# Database setup/teardown
# ------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Creates all tables in the test database at the start of the test session.
    Drops all tables after all tests finish.
    Ensures the DB schema is always clean for testing.
    """
    Base.metadata.create_all(bind=engine)
    yield
    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
        Base.metadata.drop_all(bind=conn)
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))

# -------------------------------
# Isolated SQLAlchemy session per test module
# -------------------------------
@pytest.fixture(scope="module")
def db_session():
    """
    Provides an isolated SQLAlchemy session for each test module.
    All changes are rolled back after the module's tests complete.
    Keeps the test database clean and avoids test cross-contamination.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

# ---------------------------------
# FastAPI TestClient with test DB
# ---------------------------------
@pytest.fixture(scope="module")
def client(db_session):
    """
    Provides a FastAPI TestClient for API tests, using the test database.
    Overrides FastAPI's get_db dependency so all endpoints use the test session.
    Cleans up overrides after tests.
    """
    from app.api.deps import get_db

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
