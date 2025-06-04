"""
app/models/client.py

SQLAlchemy Client model for the 'klientai' table.

Author: Ivan Bruner <ivan.bruner@stud.viko.lt>

Description:
    Defines the Client ORM model, its fields, and relationships for car rental clients.
"""
from sqlalchemy import Column, Integer, String, Date, DateTime
from app.db.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Client(Base):
    """
    SQLAlchemy ORM model for representing a client in the 'klientai' table.

    Attributes:
        kliento_id (int): Primary key.
        vardas (str): Client's first name.
        pavarde (str): Client's last name.
        el_pastas (str): Email address (unique, required).
        telefono_nr (str): Phone number.
        gimimo_data (Date): Date of birth.
        registracijos_data (DateTime): Registration date.
        bonus_taskai (int): Loyalty bonus points.
        uzsakymai (list): Relationship to Order.
        uzklausos (list): Relationship to ClientSupport.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    __tablename__ = "klientai"

    kliento_id = Column(Integer, primary_key=True, index=True)
    vardas = Column(String(50))
    pavarde = Column(String(50))
    el_pastas = Column(String(100), unique=True, index=True, nullable=False)
    telefono_nr = Column(String(20))
    gimimo_data = Column(Date)
    registracijos_data = Column(DateTime, default=datetime.utcnow)
    bonus_taskai = Column(Integer)

    uzsakymai = relationship("Order", back_populates="klientas")
    uzklausos = relationship("ClientSupport", back_populates="kliento")
