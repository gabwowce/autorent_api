from sqlalchemy import Column, Integer, Date, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Order(Base):
    __tablename__ = "uzsakymai"

    uzsakymo_id = Column(Integer, primary_key=True, index=True)
    kliento_id = Column(Integer, ForeignKey("klientai.kliento_id"))  # 👈 svarbu atitikti tikslų FK!
    automobilio_id = Column(Integer, ForeignKey("automobiliai.automobilio_id"))  # jei lentelė 'automobiliai'
    darbuotojo_id = Column(Integer, ForeignKey("darbuotojai.darbuotojo_id"))
    nuomos_data = Column(Date)
    grazinimo_data = Column(Date)
    paemimo_vietos_id = Column(Integer)
    grazinimo_vietos_id = Column(Integer)
    bendra_kaina = Column(Integer)
    uzsakymo_busena = Column(String)
    turi_papildomas_paslaugas = Column(Boolean)

    # Santykiai
    saskaita = relationship("Invoice", back_populates="uzsakymas", uselist=False)
    klientas = relationship("Client", back_populates="uzsakymai")
