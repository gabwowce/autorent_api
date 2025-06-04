"""
app/main.py

Main FastAPI application entrypoint for the Car Rental API.

Authors:
    Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    Ivan Bruner <ivan.bruner@stud.viko.lt>
    
Description:
    Initializes the FastAPI app, loads environment variables,
    sets up SQLAlchemy models, configures CORS, and registers all API routers
    for authentication, employees, cars, reservations, orders, clients, client support,
    invoices, weather, and geocoding endpoints.

Usage:
    Run the application with:
        uvicorn app.main:app --reload

Note:
    - All routers are registered under the /api/v1 prefix.
    - CORS is configured to allow requests from the frontend at http://localhost:3000.
    - Environment variables are loaded from a .env file.
"""
from fastapi import FastAPI
from app.api.v1.endpoints import auth, employee, car, reservation, order, geocode, client, client_support, invoice, weather
from app.db.base import Base
from app.db.session import engine
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Car Rental API")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(employee.router, prefix="/api/v1", tags=["Employees"])
app.include_router(car.router, prefix="/api/v1", tags=["Cars"])
app.include_router(reservation.router, prefix="/api/v1", tags=["Reservation"])
app.include_router(order.router, prefix="/api/v1", tags=["Order"])
app.include_router(client.router, prefix="/api/v1", tags=["Client"])
app.include_router(client_support.router, prefix="/api/v1", tags=["Client Support"])
app.include_router(invoice.router, prefix="/api/v1", tags=["Invoices"])
app.include_router(weather.router, prefix="/api/v1", tags=["Weather"])
app.include_router(geocode.router,  prefix="/api/v1", tags=["Geo Code"])
