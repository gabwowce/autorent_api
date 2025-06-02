from fastapi import FastAPI
from app.api.v1.endpoints import auth, employee, car, order, geocode, client, invoice, weather
from app.db.base import Base
from app.db.session import engine
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Car Rental API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(employee.router, prefix="/api/v1", tags=["Employees"])
app.include_router(car.router, prefix="/api/v1", tags=["Cars"])
app.include_router(order.router, prefix="/api/v1", tags=["Order"])
app.include_router(client.router, prefix="/api/v1", tags=["Client"])
app.include_router(invoice.router, prefix="/api/v1", tags=["Invoices"])
app.include_router(weather.router, prefix="/api/v1", tags=["Weather"])
app.include_router(geocode.router,  prefix="/api/v1", tags=["Geo Code"])