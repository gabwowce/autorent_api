from fastapi import FastAPI
from app.api.v1.endpoints import auth, employee, car
from app.models.employee import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Rental API")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(employee.router, prefix="/api/v1/employees", tags=["Employees"])
app.include_router(car.router, prefix="/api/v1/cars", tags=["Cars"])

