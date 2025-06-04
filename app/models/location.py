"""
app/models/location.py

SQLAlchemy Location model for the 'pristatymo_vietos' table.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Defines the Location ORM model, its fields, and mappings for car pick-up and drop-off places.
"""
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Location(Base):
    """
    SQLAlchemy ORM model for representing a location in the 'pristatymo_vietos' table.

    Attributes:
        vietos_id (int): Primary key.
        pavadinimas (str): Location name.
        adresas (str): Location address.
        miestas (str): City.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    __tablename__ = "pristatymo_vietos"

    vietos_id = Column(Integer, primary_key=True, index=True)
    pavadinimas = Column(String(100), nullable=False)
    adresas = Column(String(255), nullable=False)
    miestas = Column(String(100), nullable=False)
