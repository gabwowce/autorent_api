"""
app/repositories/car.py

Repository layer for car-related database operations.

Author: Gabrielė Tamaševičiūtė <gabriele.tamaseviciutes@stud.viko.lt>

Description:
    Provides functions for interacting with the Automobiliai table:
    create, read, update, delete, search, status update, and statistics.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.car import Car

def get_all(db: Session):
    """
    Retrieve all cars from the database.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        list[Car]: All car records.
    """
    return db.query(Car).all()

def get_by_id(db: Session, car_id: int):
    """
    Get a car by its ID.

    Args:
        db (Session): SQLAlchemy session.
        car_id (int): Car ID.

    Returns:
        Car | None: Car object or None if not found.
    """
    return db.query(Car).filter(Car.automobilio_id == car_id).first()

def create(db: Session, data: dict):
    """
    Create a new car record.

    Args:
        db (Session): SQLAlchemy session.
        data (dict): Car fields.

    Returns:
        Car: Newly created car.
    """
    car = Car(**data)
    db.add(car)
    db.commit()
    db.refresh(car)
    return car

def update(db: Session, car_id: int, updates: dict):
    """
    Update an existing car by ID.

    Args:
        db (Session): SQLAlchemy session.
        car_id (int): Car ID.
        updates (dict): Fields to update.

    Returns:
        Car | None: Updated car or None if not found.
    """
    car = get_by_id(db, car_id)
    if not car:
        return None
    for key, value in updates.items():
        setattr(car, key, value)
    db.commit()
    db.refresh(car)
    return car

def delete(db: Session, car_id: int):
    """
    Delete a car by ID.

    Args:
        db (Session): SQLAlchemy session.
        car_id (int): Car ID.

    Returns:
        Car | None: Deleted car or None if not found.
    """
    car = get_by_id(db, car_id)
    if not car:
        return None
    db.delete(car)
    db.commit()
    return car

def update_status(db: Session, car_id: int, status: str):
    """
    Update car status field.

    Args:
        db (Session): SQLAlchemy session.
        car_id (int): Car ID.
        status (str): New status.

    Returns:
        Car | None: Updated car or None if not found.
    """
    car = get_by_id(db, car_id)
    if not car:
        return None
    car.automobilio_statusas = status
    db.commit()
    return car

def get_car_counts_by_status(db: Session):
    """
    Get a count of cars grouped by their status.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        list[dict]: Status and count pairs.
    """
    results = (
        db.query(Car.automobilio_statusas, func.count().label("value"))
        .group_by(Car.automobilio_statusas)
        .all()
    )

    status_map = {
        "laisvas": "Laisvi",
        "servise": "Servise",
        "isnuomotas": "Išnuomoti"
    }

    return [
        {"name": status_map.get(status, status.capitalize()), "value": count}
        for status, count in results
    ]

def search_cars(
    db: Session,
    marke: str = None,
    modelis: str = None,
    spalva: str = None,
    status: str = None,
    kuro_tipas: str = None,
    metai: int = None,
    sedimos_vietos: int = None
):
    """
    Search for cars using optional filters.

    Args:
        db (Session): SQLAlchemy session.
        marke (str): Brand.
        modelis (str): Model.
        spalva (str): Color.
        status (str): Status.
        kuro_tipas (str): Fuel type.
        metai (int): Year.
        sedimos_vietos (int): Seat count.

    Returns:
        list[Car]: Filtered cars matching criteria.
    """
    query = db.query(Car)

    if marke:
        query = query.filter(Car.marke.ilike(f"%{marke}%"))
    if modelis:
        query = query.filter(Car.modelis.ilike(f"%{modelis}%"))
    if spalva:
        query = query.filter(Car.spalva.ilike(f"%{spalva}%"))
    if status:
        query = query.filter(Car.automobilio_statusas == status)
    if kuro_tipas:
        query = query.filter(Car.kuro_tipas.ilike(f"%{kuro_tipas}%"))
    if metai:
        query = query.filter(Car.metai == metai)
    if sedimos_vietos:
        query = query.filter(Car.sedimos_vietos == sedimos_vietos)

    return query.all()
