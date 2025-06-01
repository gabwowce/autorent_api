from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas import reservation as schemas
from app.repositories import reservation as repo
from utils.hateoas import generate_links
from typing import Optional
from datetime import date

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)

@router.get("/", response_model=list[schemas.ReservationOut], operation_id="getAllReservations")
def get_all_reservations(db: Session = Depends(get_db)):
    reservations = repo.get_all(db)
    return [
        {
            **res.__dict__,
            "links": [
                {"rel": "self", "href": f"/reservations/{res.rezervacijos_id}"},
                {"rel": "client", "href": f"/clients/{res.kliento_id}"},
                {"rel": "car", "href": f"/cars/{res.automobilio_id}"}
            ]
        }
        for res in reservations
    ]


@router.get("/{rezervacijos_id}", response_model=schemas.ReservationOut, operation_id="getReservationById")
def get_reservation(rezervacijos_id: int, db: Session = Depends(get_db)):
    res = repo.get_by_id(db, rezervacijos_id)
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {
        **res.__dict__,
        "links": generate_links("reservations", res.rezervacijos_id, ["delete"])
    }

@router.post("/", response_model=schemas.ReservationOut, operation_id="createReservation")
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    created = repo.create(db, reservation)
    return {
        **created.__dict__,
        "links": generate_links("reservations", created.rezervacijos_id, ["delete"])
    }

@router.delete("/{rezervacijos_id}", operation_id="deleteReservation")
def delete_reservation(rezervacijos_id: int, db: Session = Depends(get_db)):
    success = repo.delete(db, rezervacijos_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"ok": True}

@router.get("/latest", response_model=list[schemas.ReservationSummary], operation_id="getLatestReservations")
def get_latest_reservations(db: Session = Depends(get_db), limit: int = 5):
    results = repo.get_latest_reservations_with_details(db, limit=limit)
    return [
        {
            "rezervacijos_id": r.rezervacijos_id,
            "rezervacijos_pradzia": r.rezervacijos_pradzia,
            "rezervacijos_pabaiga": r.rezervacijos_pabaiga,
            "marke": r.marke,
            "modelis": r.modelis,
            "vardas": r.vardas,
            "pavarde": r.pavarde,
            "links": [
                {"rel": "self", "href": f"/reservations/{r.rezervacijos_id}"},
                {"rel": "client", "href": f"/clients/{r.kliento_id}"},
                {"rel": "car", "href": f"/cars/{r.automobilio_id}"}
            ]
        }
        for r in results
    ]

@router.get("/search", response_model=list[schemas.ReservationOut], operation_id="searchReservations")
def search_reservations(
    db: Session = Depends(get_db),
    kliento_id: Optional[int] = None,
    automobilio_id: Optional[int] = None,
    nuo: Optional[date] = None,
    iki: Optional[date] = None,
    busena: Optional[str] = None
):
    results = repo.search_reservations(
        db,
        kliento_id=kliento_id,
        automobilio_id=automobilio_id,
        nuo=nuo,
        iki=iki,
        busena=busena
    )

    return [
        {
            **res.__dict__,
            "links": [
                {"rel": "self", "href": f"/reservations/{res.rezervacijos_id}"},
                {"rel": "client", "href": f"/clients/{res.kliento_id}"},
                {"rel": "car", "href": f"/cars/{res.automobilio_id}"}
            ]
        }
        for res in results
    ]
