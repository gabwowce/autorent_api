"""
app/models/client_support.py

SQLAlchemy ClientSupport model for the 'klientu_palaikymas' table.

Author: Ivan Bruner <ivan.bruner@stud.viko.lt>

Description:
    Defines the ClientSupport ORM model, its fields, and relationships for handling client support requests.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class ClientSupport(Base):
    """
    SQLAlchemy ORM model for representing a client support request in the 'klientu_palaikymas' table.

    Attributes:
        uzklausos_id (int): Primary key.
        kliento_id (int): Foreign key to the client.
        darbuotojo_id (int): Foreign key to the employee.
        tema (str): Support request topic.
        pranesimas (str): Message content from the client.
        atsakymas (str): Reply to the client (nullable).
        pateikimo_data (DateTime): Request submission date.
        atsakymo_data (DateTime): Answer submission date (nullable).
        kliento: Relationship to the Client.
        darbuotojas: Relationship to the Employee.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    __tablename__ = "klientu_palaikymas"

    uzklausos_id = Column(Integer, primary_key=True, index=True)
    kliento_id = Column(Integer, ForeignKey("klientai.kliento_id"))
    darbuotojo_id = Column(Integer, ForeignKey("darbuotojai.darbuotojo_id"))
    tema = Column(String(100), nullable=False)
    pranesimas = Column(String(255), nullable=False)
    atsakymas = Column(String(255), nullable=True)
    pateikimo_data = Column(DateTime)
    atsakymo_data = Column(DateTime, nullable=True)

    kliento = relationship("Client", back_populates="uzklausos")
    darbuotojas = relationship("Employee", back_populates="uzklausos")
    
