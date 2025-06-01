from sqlalchemy import Column, Integer, String, Date, DECIMAL
from app.db.base import Base
from sqlalchemy.orm import relationship

class Employee(Base):
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
