from sqlalchemy.orm import Session
from app.models.car import Car

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