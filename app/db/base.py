"""
app/db/base.py

Declarative base for SQLAlchemy models.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Defines the shared declarative base class for all ORM models in the project.
    All SQLAlchemy models should inherit from Base.
"""
from sqlalchemy.orm import declarative_base

# Sukuriamas bazinis modelis
Base = declarative_base()

# !!! ČIA SVARBU: importuoti visus modelius !!!
# Tai būtina, kad Base.metadata žinotų apie visas lenteles

def import_models():
    from app.models.car import Car
    from app.models.order import Order
    from app.models.client import Client
    from app.models.employee import Employee
    from app.models.invoice import Invoice
    from app.models.reservation import Reservation

# Jei turite dar kitų modelių (pvz., papildomų lentelių ar pagalbinių), importuokite ir juos čia!
# Pvz.:
# from app.models.service import Service
# from app.models.location import Location

