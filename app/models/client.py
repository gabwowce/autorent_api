from sqlalchemy import Column, Integer, String, Date, DateTime
from app.db.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Client(Base):
    __tablename__ = "klientai"

    kliento_id = Column(Integer, primary_key=True, index=True)
    vardas = Column(String)
    pavarde = Column(String)
    el_pastas = Column(String, unique=True, index=True)
    telefono_nr = Column(String)
    gimimo_data = Column(Date)
    registracijos_data = Column(DateTime, default=datetime.utcnow)
    bonus_taskai = Column(Integer)

    uzsakymai = relationship("Order", back_populates="klientas")
    uzklausos = relationship("ClientSupport", back_populates="kliento")
