"""
app/models/car.py

SQLAlchemy Car model for the 'Automobiliai' table.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Defines the Car ORM model, its fields, and relationships for car rental operations.
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DECIMAL, Date
from app.db.base import Base
from sqlalchemy.orm import relationship
from app.models.location import Location

class Car(Base):
    """
    SQLAlchemy ORM model for representing a car in the 'Automobiliai' table.

    Attributes:
        automobilio_id (int): Primary key.
        marke (str): Car brand.
        modelis (str): Car model.
        metai (int): Year of manufacture.
        numeris (str): Car registration number.
        vin_kodas (str): Vehicle Identification Number.
        spalva (str): Car color.
        kebulo_tipas (str): Body type.
        pavarų_deze (str): Gearbox type.
        variklio_turis (Decimal): Engine displacement.
        galia_kw (int): Engine power in kW.
        kuro_tipas (str): Fuel type.
        rida (int): Mileage.
        sedimos_vietos (int): Number of seats.
        klimato_kontrole (bool): Climate control availability.
        navigacija (bool): Navigation system availability.
        kaina_parai (Decimal): Price per day.
        automobilio_statusas (str): Car status.
        technikines_galiojimas (Date): Technical inspection validity date.
        dabartine_vieta_id (int): Foreign key to location.
        pastabos (str): Additional notes.
        lokacija (Location): Relationship to Location.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    __tablename__ = "Automobiliai"

    automobilio_id = Column(Integer, primary_key=True, index=True)
    marke = Column(String(50), nullable=False)
    modelis = Column(String(50), nullable=False)
    metai = Column(Integer, nullable=False)
    numeris = Column(String(20), unique=True, nullable=False)
    vin_kodas = Column(String(17), unique=True, nullable=False)
    spalva = Column(String(50), nullable=False)
    kebulo_tipas = Column(String(50), nullable=False)
    pavarų_deze = Column(String(50), nullable=False)
    variklio_turis = Column(DECIMAL(3,1), nullable=False)
    galia_kw = Column(Integer, nullable=False)
    kuro_tipas = Column(String(20), nullable=False)
    rida = Column(Integer, nullable=False)
    sedimos_vietos = Column(Integer, nullable=False)
    klimato_kontrole = Column(Boolean, nullable=False, default=False)
    navigacija = Column(Boolean, nullable=False, default=False)
    kaina_parai = Column(DECIMAL(10,2), nullable=False)
    automobilio_statusas = Column(String(50), nullable=False)
    technikines_galiojimas = Column(Date, nullable=False)
    dabartine_vieta_id = Column(Integer, ForeignKey("pristatymo_vietos.vietos_id"))
    pastabos = Column(String(255))

    lokacija = relationship(Location, backref="automobiliai")