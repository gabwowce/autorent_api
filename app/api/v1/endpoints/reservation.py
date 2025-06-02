"""
app/api/v1/endpoints/reservation.py

API endpoints for reservation CRUD operations and advanced queries.

Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

Description:
    Implements RESTful API routes for reservation management: create, read, delete, get latest, and search.
    All responses include HATEOAS links for frontend navigation and API discoverability.
"""
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
    """
    v1/endpoints/reservation.py

    API endpoints for reservation CRUD operations and advanced queries.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>

    Description:
        Implements RESTful API routes for reservation management: create, read, delete, get latest, and search.
        All responses include HATEOAS links for frontend navigation and API discoverability.
    """
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
    """
    Retrieve all reservations.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        list[ReservationOut]: List of all reservations with HATEOAS links.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    res = repo.get_by_id(db, rezervacijos_id)
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {
        **res.__dict__,
        "links": generate_links("reservations", res.rezervacijos_id, ["delete"])
    }

@router.post("/", response_model=schemas.ReservationOut, operation_id="createReservation")
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    """
    Create a new reservation.

    Args:
        reservation (ReservationCreate): Reservation creation schema.
        db (Session): SQLAlchemy session.

    Returns:
        ReservationOut: Created reservation with HATEOAS links.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    created = repo.create(db, reservation)
    return {
        **created.__dict__,
        "links": generate_links("reservations", created.rezervacijos_id, ["delete"])
    }

@router.delete("/{rezervacijos_id}", operation_id="deleteReservation")
def delete_reservation(rezervacijos_id: int, db: Session = Depends(get_db)):
    """
    Delete a reservation by ID.

    Args:
        rezervacijos_id (int): Reservation identifier.
        db (Session): SQLAlchemy session.

    Returns:
        dict: Confirmation of deletion.

    Raises:
        HTTPException: If reservation is not found.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
    success = repo.delete(db, rezervacijos_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"ok": True}

@router.get("/latest", response_model=list[schemas.ReservationSummary], operation_id="getLatestReservations")
def get_latest_reservations(db: Session = Depends(get_db), limit: int = 5):
    """
    Get the latest reservations with details.

    Args:
        db (Session): SQLAlchemy session.
        limit (int, optional): Maximum number of reservations to return. Default is 5.

    Returns:
        list[ReservationSummary]: List of the latest reservations with HATEOAS links.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
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
    """
    Search for reservations by multiple filters.

    Args:
        db (Session): SQLAlchemy session.
        kliento_id (int, optional): Client identifier filter.
        automobilio_id (int, optional): Car identifier filter.
        nuo (date, optional): Start date filter.
        iki (date, optional): End date filter.
        busena (str, optional): Reservation status filter.

    Returns:
        list[ReservationOut]: List of reservations with HATEOAS links.

    Author: Vytautas Petronis <vytautas.petronis@stud.viko.lt>
    """
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
