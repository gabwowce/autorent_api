"""
app/repositories/order.py

Repository functions for Order entity database operations.

Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>

Description:
    Provides CRUD operations and utility queries for Order objects using SQLAlchemy.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.order import Order
from app.schemas.order import OrderCreate

def get_all(db: Session):
    """
    Retrieve all order records from the database.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Order]: List of all orders.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    return db.query(Order).all()

def get_by_id(db: Session, uzsakymo_id: int):
    """
    Retrieve an order by its unique ID.

    Args:
        db (Session): SQLAlchemy session.
        uzsakymo_id (int): Order ID.

    Returns:
        Order or None: Order object if found, otherwise None.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    return db.query(Order).filter(Order.uzsakymo_id == uzsakymo_id).first()

def get_by_client_id(db: Session, kliento_id: int):
    """
    Retrieve all orders for a specific client.

    Args:
        db (Session): SQLAlchemy session.
        kliento_id (int): Client ID.

    Returns:
        List[Order]: List of orders for the specified client.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    return db.query(Order).filter(Order.kliento_id == kliento_id).all()

def create(db: Session, order: OrderCreate):
    """
    Create a new order record in the database.

    Args:
        db (Session): SQLAlchemy session.
        order (OrderCreate): Pydantic schema with order data.

    Returns:
        Order: The created order object.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete(db: Session, uzsakymo_id: int):
    """
    Delete an order record from the database.

    Args:
        db (Session): SQLAlchemy session.
        uzsakymo_id (int): Order ID.

    Returns:
        bool: True if deleted successfully, False if not found.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    order = get_by_id(db, uzsakymo_id)
    if order:
        db.delete(order)
        db.commit()
        return True
    return False

def get_order_counts_by_status(db: Session):
    """
    Retrieve a count of orders grouped by their status.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[dict]: List of dicts with status names and counts.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    results = (
        db.query(Order.uzsakymo_busena, func.count().label("value"))
        .group_by(Order.uzsakymo_busena)
        .all()
    )

    status_map = {
        "vykdomas": "Vykdomi",
        "užbaigtas": "Užbaigti",
        "atšauktas": "Atšaukti"
    }

    return [
        {"name": status_map.get(busena, busena), "value": count}
        for busena, count in results
    ]
