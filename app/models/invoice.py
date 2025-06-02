"""
app/models/invoice.py

SQLAlchemy Invoice model for the 'saskaitos' table.

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Defines the Invoice ORM model, its fields, and relationship to the Order model for car rental invoices.
"""
from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.order import Order

class Invoice(Base):
    """
    SQLAlchemy ORM model for representing an invoice in the 'saskaitos' table.

    Attributes:
        saskaitos_id (int): Primary key.
        uzsakymo_id (int): Foreign key to the related order.
        suma (float): Total invoice amount.
        saskaitos_data (Date): Date the invoice was issued.
        uzsakymas (Order): Relationship to the associated Order.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    __tablename__ = "saskaitos"

    saskaitos_id = Column(Integer, primary_key=True, index=True)
    uzsakymo_id = Column(Integer, ForeignKey("uzsakymai.uzsakymo_id"))
    suma = Column(Float, nullable=False)
    saskaitos_data = Column(Date, nullable=False)

    uzsakymas = relationship(Order, back_populates="saskaita")
