"""
app/api/v1/endpoints/order.py

API endpoints for order CRUD operations and statistics.

Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>

Description:
    Implements RESTful API routes for order management: create, read, delete, statistics by status, and filter by client.
    All responses include HATEOAS links for easier navigation from the frontend.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas import order as schemas
from app.repositories import order as repo
from utils.hateoas import generate_links
from app.api.deps import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=list[schemas.OrderOut], operation_id="getAllOrders")
def get_all_orders(db: Session = Depends(get_db)):
    """
    Retrieve all orders.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        list[OrderOut]: List of orders with HATEOAS links.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
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
    """
    Retrieve an order by ID.

    Args:
        uzsakymo_id (int): Order identifier.
        db (Session): SQLAlchemy session.

    Returns:
        OrderOut: Order data with HATEOAS links.

    Raises:
        HTTPException: If order is not found.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
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
    """
    Create a new order.

    Args:
        order (OrderCreate): Order creation schema.
        db (Session): SQLAlchemy session.

    Returns:
        OrderOut: Created order with HATEOAS links.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
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
    """
    Delete an order by ID.

    Args:
        uzsakymo_id (int): Order identifier.
        db (Session): SQLAlchemy session.

    Returns:
        dict: Confirmation of deletion.

    Raises:
        HTTPException: If order is not found.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    success = repo.delete(db, uzsakymo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"ok": True}

@router.get("/stats/by-status", operation_id="getOrderStatsByStatus")
def get_order_stats_by_status(db: Session = Depends(get_db)):
    """
    Get order statistics grouped by status.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        list[dict]: Aggregated counts per status.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    return repo.get_order_counts_by_status(db)

@router.get("/by-client/{kliento_id}", response_model=list[schemas.OrderOut], operation_id="getOrderByClient")
def get_orders_by_client(kliento_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all orders for a specific client.

    Args:
        kliento_id (int): Client identifier.
        db (Session): SQLAlchemy session.

    Returns:
        list[OrderOut]: List of orders with HATEOAS links.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
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


@router.put("/{uzsakymo_id}", response_model=schemas.OrderOut, operation_id="updateOrder")
def update_order(uzsakymo_id: int, order_update: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order = repo.get_by_id(db, uzsakymo_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    # Čia logika kaip updatinti
    if order_update.uzsakymo_busena is not None:
        order.uzsakymo_busena = order_update.uzsakymo_busena
    if order_update.grazinimo_data is not None:
        order.grazinimo_data = order_update.grazinimo_data
    if order_update.turi_papildomas_paslaugas is not None:
        order.turi_papildomas_paslaugas = order_update.turi_papildomas_paslaugas
    db.commit()
    db.refresh(order)
    return {
        **order.__dict__,
        "links": [
            {"rel": "self", "href": f"/orders/{order.uzsakymo_id}"},
            {"rel": "client", "href": f"/clients/{order.kliento_id}"},
            {"rel": "car", "href": f"/cars/{order.automobilio_id}"},
            {"rel": "delete", "href": f"/orders/{order.uzsakymo_id}"}
        ]
    }
