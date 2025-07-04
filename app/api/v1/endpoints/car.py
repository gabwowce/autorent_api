"""
app/api/v1/endpoints/cars.py

API endpoints for managing car data in the rental system.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Provides CRUD operations and search functionality for cars.
    Includes support for location data and HATEOAS links for each resource.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List

from app.api.deps import get_db
from app.models.car import Car
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List

from app.api.deps import get_db
from app.models.car import Car
from app.schemas.car import CarOut, CarCreate, CarUpdate, CarStatusUpdate
from utils.hateoas import generate_links
from app.api.deps import get_current_user

router = APIRouter(
    prefix="/cars",
    tags=["Cars"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=List[CarOut], operation_id="getAllCars")
def get_all_cars(db: Session = Depends(get_db)):
    """
    Retrieve all cars with their location and HATEOAS links.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[CarOut]: List of all cars.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>
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
            "links": generate_links("cars", car.automobilio_id, ["update", "delete", "update_status"]),
        }
        for car in cars
    ]

@router.get("/search", response_model=List[CarOut], operation_id="searchCars")
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
    Search for cars using optional filters.

    Args:
        db (Session): SQLAlchemy session.
        marke (str): Car brand.
        modelis (str): Car model.
        spalva (str): Color.
        status (str): Car status.
        kuro_tipas (str): Fuel type.
        metai (int): Year.
        sedimos_vietos (int): Seats.

    Returns:
        List[CarOut]: Filtered list of cars with HATEOAS links.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>
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
            "links": generate_links("cars", car.automobilio_id, ["update", "delete", "update_status"]),
        }
        for car in cars
    ]

@router.get("/{car_id}", response_model=CarOut, operation_id="getCarById")
def get_car(car_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific car by ID.

    Args:
        car_id (int): Car ID.
        db (Session): SQLAlchemy session.

    Returns:
        CarOut: Car details.

    Raises:
        HTTPException: If car not found.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>
    """
    car = db.query(Car).options(joinedload(Car.lokacija)).filter(Car.automobilio_id == car_id).first()
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
        "links": generate_links("cars", car.automobilio_id, ["update", "delete", "update_status"]),
    }

@router.post("/", response_model=CarOut, operation_id="createCar")
def create_car(data: CarCreate, db: Session = Depends(get_db)):
    """
    Create a new car record.

    Args:
        data (CarCreate): New car data.
        db (Session): SQLAlchemy session.

    Returns:
        CarOut: Created car with HATEOAS links.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>
    """
    car = Car(**data.dict())
    db.add(car)
    db.commit()
    db.refresh(car)
    return {
        **car.__dict__,
        "lokacija": None,
        "links": generate_links("cars", car.automobilio_id, ["update", "delete", "update_status"]),
    }

@router.put("/{car_id}", response_model=CarOut, operation_id="updateCar")
def update_car(car_id: int, data: CarUpdate, db: Session = Depends(get_db)):
    """
    Update an existing car by ID.

    Args:
        car_id (int): Car ID.
        data (CarUpdate): Updated fields.
        db (Session): SQLAlchemy session.

    Returns:
        CarOut: Updated car with HATEOAS links.

    Raises:
        HTTPException: If car not found.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>
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
        "links": generate_links("cars", car.automobilio_id, ["update", "delete", "update_status"]),
    }

@router.patch("/{car_id}/status", response_model=CarOut, operation_id="updateCarStatus")
def update_car_status(car_id: int, data: CarStatusUpdate, db: Session = Depends(get_db)):
    """
    Update status of a car.

    Args:
        car_id (int): Car ID.
        data (CarStatusUpdate): New status.
        db (Session): SQLAlchemy session.

    Returns:
        CarOut: Updated car with new status and HATEOAS links.

    Raises:
        HTTPException: If car not found.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>
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
        "links": generate_links("cars", car.automobilio_id, ["update", "delete", "update_status"]),
    }

@router.delete("/{car_id}", operation_id="deleteCar")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    """
    Delete a car by ID.
sea
    Args:
        car_id (int): Car ID.
        db (Session): SQLAlchemy session.

    Returns:
        dict: Deletion success message.

    Raises:
        HTTPException: If car not found.

    Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>
    """
    car = db.query(Car).filter(Car.automobilio_id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(car)
    db.commit()
    return {"message": "Car deleted successfully"}