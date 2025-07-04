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
from fastapi import FastAPI, Request
from app.api.v1.endpoints import auth, employee, car, reservation, order, geocode, client, client_support, invoice
from app.db.base import Base
from app.db.session import engine
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, SecurityScheme

load_dotenv()

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Car Rental API")
# Token schema
from fastapi.openapi.models import SecurityScheme
from fastapi.openapi.utils import get_openapi
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        description="API documentation",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema


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
app.include_router(reservation.router, prefix="/api/v1", tags=["Reservations"])
app.include_router(order.router, prefix="/api/v1", tags=["Orders"])
app.include_router(client.router, prefix="/api/v1", tags=["Client"])
app.include_router(client_support.router, prefix="/api/v1", tags=["Client Support"])
app.include_router(invoice.router, prefix="/api/v1", tags=["Invoices"])
app.include_router(geocode.router,  prefix="/api/v1", tags=["Geo Code"])

@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    import traceback
    tb = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    print(tb)  # Kad matytum konsolėje
    return PlainTextResponse(tb, status_code=500)