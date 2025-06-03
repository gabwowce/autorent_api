"""
app/models/geocode.py

SQLAlchemy model(s) for geocoding-related database tables.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Šiame modulyje būtų aprašyti SQLAlchemy ORM modeliai, skirti geokodavimo (adreso-koordinatės) informacijai saugoti, jei tokia informacija būtų laikoma duomenų bazėje.
    Paprastai geokodavimo operacijos atliekamos „on the fly“ per API ir nėra saugomos DB, tačiau, jei reikia saugoti adresų užklausas ar cache’inamas koordinates, čia aprašytumėte modelius, pvz.:

    - GeocodeRequest: užklausos su adresu saugojimas.
    - GeocodeResult: adresas, latitude, longitude, timestamp ir t.t.

Usage:
    Sukurkite atitinkamus modelius, jei norite išsaugoti geokodavimo užklausų istoriją ar cache.

Pavyzdinis modelio šablonas:
    from sqlalchemy import Column, Integer, String, Float, DateTime
    from app.db.base import Base
    from datetime import datetime

    class GeocodeResult(Base):
        __tablename__ = "geocode_results"
        id = Column(Integer, primary_key=True, index=True)
        adresas = Column(String(255), nullable=False)
        lat = Column(Float, nullable=False)
        lng = Column(Float, nullable=False)
        timestamp = Column(DateTime, default=datetime.utcnow)

        # Čia galima aprašyti papildomus laukus pagal poreikį.
"""