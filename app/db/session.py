"""
app/db/session.py

Database engine and session configuration.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Creates a SQLAlchemy engine using a database URL from environment variables.
    Provides a reusable session factory (SessionLocal) for dependency injection.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Fallback lokalus adresas, jei .env nėra
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:1234@localhost:3306/autorentdb")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
