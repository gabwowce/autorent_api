from sqlalchemy.orm import Session
from app.models.employee import Employee

def get_by_email(db: Session, email: str):
    return db.query(Employee).filter(Employee.el_pastas == email).first()


def get_by_id(db: Session, darbuotojo_id: int):
    return db.query(Employee).filter(Employee.darbuotojo_id == darbuotojo_id).first()

def create_employee(db: Session, data: dict):
    naujas = Employee(**data)
    db.add(naujas)
    db.commit()
    db.refresh(naujas)
    return naujas

def get_all(db: Session):
    return db.query(Employee).all()

def get_by_id(db: Session, darbuotojo_id: int):
    return db.query(Employee).filter(Employee.darbuotojo_id == darbuotojo_id).first()
