from sqlalchemy import Column, Integer, String, Date, DECIMAL
from app.db.base import Base
from sqlalchemy.orm import relationship

class Employee(Base):
    __tablename__ = "darbuotojai"

    darbuotojo_id = Column(Integer, primary_key=True, index=True)
    vardas = Column(String)
    pavarde = Column(String)
    el_pastas = Column(String, unique=True, index=True)
    telefono_nr = Column(String)
    pareigos = Column(String)
    atlyginimas = Column(DECIMAL)
    isidarbinimo_data = Column(Date)
    slaptazodis = Column(String)

    uzklausos = relationship("ClientSupport", back_populates="darbuotojas")
