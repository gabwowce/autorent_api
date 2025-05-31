from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.order import Order

class Invoice(Base):
    __tablename__ = "saskaitos"

    saskaitos_id = Column(Integer, primary_key=True, index=True)
    uzsakymo_id = Column(Integer, ForeignKey("uzsakymai.uzsakymo_id"))
    suma = Column(Float, nullable=False)
    saskaitos_data = Column(Date, nullable=False)

    uzsakymas = relationship(Order, back_populates="saskaita")
