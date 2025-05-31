from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas import order as schemas
from app.repositories import order as repo
from utils.hateoas import generate_links

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get("/", response_model=list[schemas.OrderOut], operation_id="getAllOrders")
def get_all_orders(db: Session = Depends(get_db)):
    orders = repo.get_all(db)
    return [
        {
            **order.__dict__,
            "links": [
                {"rel": "self", "href": f"/orders/{order.uzsakymo_id}"},
                {"rel": "client", "href": f"/clients/{order.kliento_id}"},
                {"rel": "car", "href": f"/cars/{order.automobilio_id}"},
                {"rel": "delete", "href": f"/orders/{order.uzsakymo_id}"}
            ]
        }
        for order in orders
    ]

@router.get("/{uzsakymo_id}", response_model=schemas.OrderOut, operation_id="getOrderById")
def get_order(uzsakymo_id: int, db: Session = Depends(get_db)):
    order = repo.get_by_id(db, uzsakymo_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        **order.__dict__,
        "links": [
            {"rel": "self", "href": f"/orders/{order.uzsakymo_id}"},
            {"rel": "client", "href": f"/clients/{order.kliento_id}"},
            {"rel": "car", "href": f"/cars/{order.automobilio_id}"},
            {"rel": "delete", "href": f"/orders/{order.uzsakymo_id}"}
        ]
    }

@router.post("/", response_model=schemas.OrderOut, operation_id="createOrder")
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    created = repo.create(db, order)
    return {
        **created.__dict__,
        "links": [
            {"rel": "self", "href": f"/orders/{created.uzsakymo_id}"},
            {"rel": "client", "href": f"/clients/{created.kliento_id}"},
            {"rel": "car", "href": f"/cars/{created.automobilio_id}"},
            {"rel": "delete", "href": f"/orders/{created.uzsakymo_id}"}
        ]
    }

@router.delete("/{uzsakymo_id}", operation_id="deleteOrder")
def delete_order(uzsakymo_id: int, db: Session = Depends(get_db)):
    success = repo.delete(db, uzsakymo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"ok": True}

@router.get("/stats/by-status", operation_id="getOrderStatsByStatus")
def get_order_stats_by_status(db: Session = Depends(get_db)):
    return repo.get_order_counts_by_status(db)

@router.get("/by-client/{kliento_id}", response_model=list[schemas.OrderOut], operation_id="getOrderByClient")
def get_orders_by_client(kliento_id: int, db: Session = Depends(get_db)):
    orders = repo.get_by_client_id(db, kliento_id)
    return [
        {
            **order.__dict__,
            "links": [
                {"rel": "self", "href": f"/orders/{order.uzsakymo_id}"},
                {"rel": "client", "href": f"/clients/{order.kliento_id}"},
                {"rel": "car", "href": f"/cars/{order.automobilio_id}"},
                {"rel": "delete", "href": f"/orders/{order.uzsakymo_id}"}
            ]
        }
        for order in orders
    ]
