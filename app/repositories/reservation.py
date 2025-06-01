from datetime import date
from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate
from sqlalchemy import desc
from app.models.reservation import Reservation
from app.models.car import Car
from app.models.client import Client



def get_all(db: Session):
    return db.query(Reservation).all()

def get_by_id(db: Session, rezervacijos_id: int):
    return db.query(Reservation).filter(Reservation.rezervacijos_id == rezervacijos_id).first()

def create(db: Session, reservation: ReservationCreate):
    db_res = Reservation(**reservation.dict())
    db.add(db_res)
    db.commit()
    db.refresh(db_res)
    return db_res

def delete(db: Session, rezervacijos_id: int):
    db_res = get_by_id(db, rezervacijos_id)
    if db_res:
        db.delete(db_res)
        db.commit()
        return True
    return False
    
def get_latest_reservations_with_details(db: Session, limit: int = 5):
    return (
        db.query(
            Reservation.rezervacijos_id,
            Reservation.kliento_id,
            Reservation.automobilio_id,
            Reservation.rezervacijos_pradzia,
            Reservation.rezervacijos_pabaiga,
            Car.marke,
            Car.modelis,
            Client.vardas,
            Client.pavarde,
        )
        .join(Car, Reservation.automobilio_id == Car.automobilio_id)
        .join(Client, Reservation.kliento_id == Client.kliento_id)
        .order_by(desc(Reservation.rezervacijos_pradzia))
        .limit(limit)
        .all()
    )

def search_reservations(
    db: Session,
    kliento_id: int = None,
    automobilio_id: int = None,
    nuo: date = None,
    iki: date = None,
    busena: str = None
):
    query = db.query(Reservation)

    if kliento_id:
        query = query.filter(Reservation.kliento_id == kliento_id)
    if automobilio_id:
        query = query.filter(Reservation.automobilio_id == automobilio_id)
    if nuo:
        query = query.filter(Reservation.rezervacijos_pradzia >= nuo)
    if iki:
        query = query.filter(Reservation.rezervacijos_pabaiga <= iki)
    if busena:
        query = query.filter(Reservation.busena == busena)

    return query.all()

