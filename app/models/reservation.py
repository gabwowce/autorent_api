from sqlalchemy import Column, Integer, Date, String, ForeignKey
from app.db.base import Base

class Reservation(Base):
    __tablename__ = "rezervavimas"

    rezervacijos_id = Column(Integer, primary_key=True, index=True)
    kliento_id = Column(Integer, ForeignKey("klientas.id"))
    automobilio_id = Column(Integer, ForeignKey("automobilis.id"))
    rezervacijos_pradzia = Column(Date)
    rezervacijos_pabaiga = Column(Date)
    busena = Column(String)
