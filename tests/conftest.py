"""
Pytest conftest module for AutoRect

- Užkrauna testinę MySQL DB (testautorentdb)
- Visi API testai gauna TestClient su perrašytu get_db (visi repo/unit testai – švari SQLAlchemy sesija)
- Visi DB veiksmai izoliavimui rollback'inami po kiekvieno testavimo

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
"""

import pytest
from fastapi.testclient import TestClient
import os
from sqlalchemy import text

os.environ["DATABASE_URL"] = "mysql+pymysql://root:1234@localhost:3306/testautorentdb"
from app.db.base import Base
from app.db.session import SessionLocal, engine

# Priverstinai importuok visus savo modelius
import app.models

from app.main import app

# Lentelių sukurimas/pašalinimas visai testų sesijai
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
        Base.metadata.drop_all(bind=conn)
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))

# Izoliuota DB sesija kiekvienam testų moduliui
@pytest.fixture(scope="module")
def db_session():
    """Izoliuota SQLAlchemy sesija – rollback po kiekvieno testavimo."""
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

# API TestClient fixture su module scope
@pytest.fixture(scope="module")
def client(db_session):
    """FastAPI TestClient – visiems API testams, su testine DB."""

    # Override turi būti TIKRAS tavo app dependency!
    from app.db.session import get_db  # jei jis čia, arba tikslus kelias

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
