"""
app/models/reservation.py

SQLAlchemy Reservation model for the 'rezervavimas' table.

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Defines the Reservation ORM model, its fields, and relationships for reservation records in the car rental system.
"""
from sqlalchemy import Column, Integer, Date, String, ForeignKey
from app.db.base import Base

class Reservation(Base):
    """
    SQLAlchemy ORM model for representing a reservation in the 'rezervavimas' table.

    Attributes:
        rezervacijos_id (int): Primary key.
        kliento_id (int): Foreign key to the client.
        automobilio_id (int): Foreign key to the car.
        rezervacijos_pradzia (Date): Reservation start date.
        rezervacijos_pabaiga (Date): Reservation end date.
        busena (str): Reservation status.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    __tablename__ = "rezervavimas"

    rezervacijos_id = Column(Integer, primary_key=True, index=True)
    kliento_id = Column(Integer, ForeignKey("klientai.kliento_id"))
    automobilio_id = Column(Integer, ForeignKey("Automobiliai.automobilio_id"))
    rezervacijos_pradzia = Column(Date)
    rezervacijos_pabaiga = Column(Date)
    busena = Column(String(100))
