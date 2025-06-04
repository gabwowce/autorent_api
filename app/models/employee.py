"""
app/models/employee.py

SQLAlchemy Employee model for the 'darbuotojai' table.

Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>

Description:
    Defines the Employee ORM model, its fields, and relationships for employees in the car rental system.
"""
from sqlalchemy import Column, Integer, String, Date, DECIMAL
from app.db.base import Base
from sqlalchemy.orm import relationship

class Employee(Base):
    """
    SQLAlchemy ORM model for representing an employee in the 'darbuotojai' table.

    Attributes:
        darbuotojo_id (int): Primary key.
        vardas (str): Employee's first name.
        pavarde (str): Employee's last name.
        el_pastas (str): Email address (unique, required).
        telefono_nr (str): Phone number.
        pareigos (str): Position or job title.
        atlyginimas (Decimal): Salary.
        isidarbinimo_data (Date): Employment start date.
        slaptazodis (str): Password (hashed).
        uzklausos (list): Relationship to ClientSupport.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    __tablename__ = "darbuotojai"

    darbuotojo_id = Column(Integer, primary_key=True, index=True)
    vardas = Column(String(50))
    pavarde = Column(String(50))
    el_pastas = Column(String(100), unique=True, index=True, nullable=False)
    telefono_nr = Column(String(20))
    pareigos = Column(String(50))
    atlyginimas = Column(DECIMAL)
    isidarbinimo_data = Column(Date)
    slaptazodis = Column(String(255))

    uzklausos = relationship("ClientSupport", back_populates="darbuotojas")
