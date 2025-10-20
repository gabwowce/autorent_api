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
    invoices and geocoding endpoints.

Usage:
    Run the application with:
        uvicorn app.main:app --reload

Note:
    - All routers are registered under the /api/v1 prefix.
    - CORS is configured to allow requests from the frontend at http://localhost:3000.
    - Environment variables are loaded from a .env file.
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.openapi.utils import get_openapi

from app.db.base import Base
from app.db.session import engine
from app.api.v1.endpoints import (
    auth, employee, car, reservation, order, geocode, client, client_support, invoice
)

load_dotenv()

# Sukuriame DB lenteles (užtikrink, kad app.db.base importuoja visus modelius)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Rental API", version="1.0.0")

# Session (OAuthui reikalinga)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "dev-secret-32chars-change-me"),
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Swagger Bearer schema (pritaikoma visiems endpointams, kurie jos prašo)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Car Rental API",
        version="1.0.0",
        description="API documentation",
        routes=app.routes,
    )
    components = openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})
    components["BearerAuth"] = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi  # aktyvuojame custom OpenAPI

# Routeriai
app.include_router(auth.router,          prefix="/api/v1", tags=["Authentication"])
app.include_router(employee.router,      prefix="/api/v1", tags=["Employees"])
app.include_router(car.router,           prefix="/api/v1", tags=["Cars"])
app.include_router(reservation.router,   prefix="/api/v1", tags=["Reservations"])
app.include_router(order.router,         prefix="/api/v1", tags=["Orders"])
app.include_router(client.router,        prefix="/api/v1", tags=["Client"])
app.include_router(client_support.router,prefix="/api/v1", tags=["Client Support"])
app.include_router(invoice.router,       prefix="/api/v1", tags=["Invoices"])
app.include_router(geocode.router,       prefix="/api/v1", tags=["Geo Code"])

# Naudingas trace per 500
@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    import traceback
    tb = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    print(tb)
    return PlainTextResponse(tb, status_code=500)