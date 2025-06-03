"""
app/db/session.py

SQLAlchemy engine and session factory configuration.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Initializes the SQLAlchemy engine and sessionmaker for database access.
    Uses DATABASE_URL from environment variables or a default value for local development.
    All database sessions should be created using SessionLocal.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Naudojama reali konfiguracija iš .env
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:1234@localhost:3306/autorentdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)