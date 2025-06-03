"""
app/db/base.py

SQLAlchemy declarative base for model definitions.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Defines the declarative base class used by all ORM models.
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
