"""
app/models/order.py

SQLAlchemy Order model for the 'uzsakymai' table.

Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>

Description:
    Defines the Order ORM model, its fields, and relationships for car rental orders.
"""
from sqlalchemy import Column, Integer, Date, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Order(Base):
    """
    SQLAlchemy ORM model for representing an order in the 'uzsakymai' table.

    Attributes:
        uzsakymo_id (int): Primary key.
        kliento_id (int): Foreign key to the client.
        automobilio_id (int): Foreign key to the car.
        darbuotojo_id (int): Foreign key to the employee.
        nuomos_data (Date): Rental start date.
        grazinimo_data (Date): Rental end date.
        paemimo_vietos_id (int): Pick-up location ID.
        grazinimo_vietos_id (int): Drop-off location ID.
        bendra_kaina (int): Total order price.
        uzsakymo_busena (str): Order status.
        turi_papildomas_paslaugas (bool): Whether additional services are included.
        saskaita: Relationship to Invoice (one-to-one).
        klientas: Relationship to Client.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    __tablename__ = "uzsakymai"

    uzsakymo_id = Column(Integer, primary_key=True, index=True)
    kliento_id = Column(Integer, ForeignKey("klientai.kliento_id"))
    automobilio_id = Column(Integer, ForeignKey("Automobiliai.automobilio_id"))
    darbuotojo_id = Column(Integer, ForeignKey("darbuotojai.darbuotojo_id"))
    nuomos_data = Column(Date)
    grazinimo_data = Column(Date)
    paemimo_vietos_id = Column(Integer)
    grazinimo_vietos_id = Column(Integer)
    bendra_kaina = Column(Integer)
    uzsakymo_busena = Column(String(50))
    turi_papildomas_paslaugas = Column(Boolean)

    # Santykiai
    saskaita = relationship("Invoice", back_populates="uzsakymas", uselist=False)
    klientas = relationship("Client", back_populates="uzsakymai")

