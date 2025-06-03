"""
main.py

Main application entry point for the Car Rental API.

Authors:
    Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>
    Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    Ivan Bruner <ivan.bruner@stud.viko.lt>

Description:
    - Initializes FastAPI app with CORS middleware.
    - Creates database tables.
    - Registers all API routers (authentication, employees, cars, orders, etc.).
"""
from fastapi import FastAPI
from app.api.v1.endpoints import auth, employee, car, order, geocode, client, invoice, weather
from app.db.base import Base
from app.db.session import engine
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Automatiškai sukuria visas lenteles pagal SQLAlchemy modelius
Base.metadata.create_all(bind=engine)

# Inicijuojama FastAPI aplikacija
app = FastAPI(title="Car Rental API")

# CORS middleware leidžia frontend (pvz., React) pasiekti API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registruojami visi endpoint'ai
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(employee.router, prefix="/api/v1", tags=["Employees"])
app.include_router(car.router, prefix="/api/v1", tags=["Cars"])
app.include_router(order.router, prefix="/api/v1", tags=["Order"])
app.include_router(client.router, prefix="/api/v1", tags=["Client"])
app.include_router(invoice.router, prefix="/api/v1", tags=["Invoices"])
app.include_router(weather.router, prefix="/api/v1", tags=["Weather"])
app.include_router(geocode.router, prefix="/api/v1", tags=["Geo Code"])
