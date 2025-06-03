"""
app/models/location.py

SQLAlchemy ORM model representing a delivery or pickup location.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Defines the "pristatymo_vietos" table structure.
    Stores delivery/pick-up location information such as name, address, and city.
"""
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Location(Base):
    __tablename__ = "pristatymo_vietos"

    vietos_id = Column(Integer, primary_key=True, index=True)
    pavadinimas = Column(String, nullable=False)
    adresas = Column(String, nullable=False)
    miestas = Column(String, nullable=False)
