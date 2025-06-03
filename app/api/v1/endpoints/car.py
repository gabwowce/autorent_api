"""
app/api/v1/endpoints/car.py

API endpoints for car CRUD operations and search.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>

Description:
    Implements RESTful API routes for car entity management, including create, read,
    update, delete, and search operations. All endpoints use HATEOAS links and support
    relationships with location data.

Usage:
    Register this router with the main FastAPI app for car management endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List

from app.api.deps import get_db
from app.models.car import Car
from app.schemas.car import CarOut, CarCreate, CarUpdate, CarStatusUpdate
from utils.hateoas import generate_links

router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)

# ---------- CRUD + paieška ----------

@router.get(
    "/", 
    response_model=List[CarOut], 
    operation_id="getAllCars",          # <—— trumpas, aiškus ID
)
def get_all_cars(db: Session = Depends(get_db)):
    """
    Retrieve all cars with their locations.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[CarOut]: List of cars with location and HATEOAS links.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    cars = db.query(Car).options(joinedload(Car.lokacija)).all()
    return [
        {
            **car.__dict__,
            "lokacija": (
                {
                    "vietos_id": car.lokacija.vietos_id,
                    "pavadinimas": car.lokacija.pavadinimas,
                    "adresas": car.lokacija.adresas,
                    "miestas": car.lokacija.miestas,
                } if car.lokacija else None
            ),
            "links": generate_links(
                "cars", car.automobilio_id, ["update", "delete", "update_status"]
            ),
        }
        for car in cars
    ]


@router.get(
    "/{car_id}", 
    response_model=CarOut, 
    operation_id="getCarById",
)
def get_car(car_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific car by its ID, including location.

    Args:
        car_id (int): Car identifier.
        db (Session): SQLAlchemy session.

    Returns:
        CarOut: Car data with location and HATEOAS links.

    Raises:
        HTTPException: If car is not found.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    car = (
        db.query(Car)
        .options(joinedload(Car.lokacija))
        .filter(Car.automobilio_id == car_id)
        .first()
    )
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return {
        **car.__dict__,
        "lokacija": (
            {
                "vietos_id": car.lokacija.vietos_id,
                "pavadinimas": car.lokacija.pavadinimas,
                "adresas": car.lokacija.adresas,
                "miestas": car.lokacija.miestas,
            } if car.lokacija else None
        ),
        "links": generate_links(
            "cars", car.automobilio_id, ["update", "delete", "update_status"]
        ),
    }


@router.post(
    "/", 
    response_model=CarOut, 
    operation_id="createCar",
)
def create_car(data: CarCreate, db: Session = Depends(get_db)):
    """
    Create a new car record.

    Args:
        data (CarCreate): Car creation schema.
        db (Session): SQLAlchemy session.

    Returns:
        CarOut: Created car data with HATEOAS links.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    car = Car(**data.dict())
    db.add(car)
    db.commit()
    db.refresh(car)
    return {
        **car.__dict__,
        "lokacija": None,
        "links": generate_links(
            "cars", car.automobilio_id, ["update", "delete", "update_status"]
        ),
    }


@router.put(
    "/{car_id}", 
    response_model=CarOut, 
    operation_id="updateCar",
)
def update_car(car_id: int, data: CarUpdate, db: Session = Depends(get_db)):
    """
    Update an existing car record.

    Args:
        car_id (int): Car identifier.
        data (CarUpdate): Car update schema.
        db (Session): SQLAlchemy session.

    Returns:
        CarOut: Updated car data with location and HATEOAS links.

    Raises:
        HTTPException: If car is not found.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    car = db.query(Car).filter(Car.automobilio_id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(car, key, value)

    db.commit()
    db.refresh(car)
    return {
        **car.__dict__,
        "lokacija": (
            {
                "vietos_id": car.lokacija.vietos_id,
                "pavadinimas": car.lokacija.pavadinimas,
                "adresas": car.lokacija.adresas,
                "miestas": car.lokacija.miestas,
            } if car.lokacija else None
        ),
        "links": generate_links(
            "cars", car.automobilio_id, ["update", "delete", "update_status"]
        ),
    }


@router.patch(
    "/{car_id}/status", 
    response_model=CarOut, 
    operation_id="updateCarStatus",
)
def update_car_status(car_id: int, data: CarStatusUpdate, db: Session = Depends(get_db)):
    """
    Update the status of a car.

    Args:
        car_id (int): Car identifier.
        data (CarStatusUpdate): Car status update schema.
        db (Session): SQLAlchemy session.

    Returns:
        CarOut: Updated car data with location and HATEOAS links.

    Raises:
        HTTPException: If car is not found.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    car = db.query(Car).filter(Car.automobilio_id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    car.automobilio_statusas = data.status
    db.commit()
    db.refresh(car)
    return {
        **car.__dict__,
        "lokacija": (
            {
                "vietos_id": car.lokacija.vietos_id,
                "pavadinimas": car.lokacija.pavadinimas,
                "adresas": car.lokacija.adresas,
                "miestas": car.lokacija.miestas,
            } if car.lokacija else None
        ),
        "links": generate_links(
            "cars", car.automobilio_id, ["update", "delete", "update_status"]
        ),
    }

@router.delete(
    "/{car_id}", 
    operation_id="deleteCar",
)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.automobilio_id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(car)
    db.commit()
    return {"message": "Car deleted successfully"}


@router.get(
    "/search", 
    response_model=List[CarOut], 
    operation_id="searchCars",
)


@router.get(
    "/search", 
    response_model=List[CarOut], 
    operation_id="searchCars",
)
def search_cars(
    db: Session = Depends(get_db),
    marke: Optional[str] = None,
    modelis: Optional[str] = None,
    spalva: Optional[str] = None,
    status: Optional[str] = None,
    kuro_tipas: Optional[str] = None,
    metai: Optional[int] = None,
    sedimos_vietos: Optional[int] = None,
):
    """
    Search for cars by multiple filters.

    Args:
        db (Session): SQLAlchemy session.
        marke (str, optional): Car brand filter.
        modelis (str, optional): Car model filter.
        spalva (str, optional): Car color filter.
        status (str, optional): Car status filter.
        kuro_tipas (str, optional): Fuel type filter.
        metai (int, optional): Year filter.
        sedimos_vietos (int, optional): Number of seats filter.

    Returns:
        List[CarOut]: List of cars matching search with HATEOAS links.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciute@stud.viko.lt>
    """
    query = db.query(Car).options(joinedload(Car.lokacija))

    if marke:
        query = query.filter(Car.marke.ilike(f"%{marke}%"))
    if modelis:
        query = query.filter(Car.modelis.ilike(f"%{modelis}%"))
    if spalva:
        query = query.filter(Car.spalva.ilike(f"%{spalva}%"))
    if status:
        query = query.filter(Car.automobilio_statusas == status)
    if kuro_tipas:
        query = query.filter(Car.kuro_tipas == kuro_tipas)
    if metai:
        query = query.filter(Car.metai == metai)
    if sedimos_vietos:
        query = query.filter(Car.sedimos_vietos == sedimos_vietos)

    cars = query.all()

    return [
        {
            **car.__dict__,
            "lokacija": (
                {
                    "vietos_id": car.lokacija.vietos_id,
                    "pavadinimas": car.lokacija.pavadinimas,
                    "adresas": car.lokacija.adresas,
                    "miestas": car.lokacija.miestas,
                } if car.lokacija else None
            ),
            "links": generate_links(
                "cars", car.automobilio_id, ["update", "delete", "update_status"]
            ),
        }
        for car in cars
    ]
