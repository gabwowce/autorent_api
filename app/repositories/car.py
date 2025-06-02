from sqlalchemy.orm import Session
from app.models.car import Car
from sqlalchemy import func

def get_all(db: Session):
    return db.query(Car).all()

def get_by_id(db: Session, car_id: int):
    return db.query(Car).filter(Car.automobilio_id == car_id).first()

def create(db: Session, data: dict):
    car = Car(**data)
    db.add(car)
    db.commit()
    db.refresh(car)
    return car

def update(db: Session, car_id: int, updates: dict):
    car = get_by_id(db, car_id)
    if not car:
        return None
    for key, value in updates.items():
        setattr(car, key, value)
    db.commit()
    db.refresh(car)
    return car

def delete(db: Session, car_id: int):
    car = get_by_id(db, car_id)
    if not car:
        return None
    db.delete(car)
    db.commit()
    return car

def update_status(db: Session, car_id: int, status: str):
    car = get_by_id(db, car_id)
    if not car:
        return None
    car.automobilio_statusas = status
    db.commit()
    return car

def get_car_counts_by_status(db: Session):
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
