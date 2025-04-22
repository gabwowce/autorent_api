from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Naudojama reali konfiguracija iš .env
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:12301@localhost:3306/autorentdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)