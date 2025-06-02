"""
app/repositories/client.py

Repository functions for Client entity database operations.

Author: Ivan Bruner <ivan.bruner@stud.viko.lt>

Description:
    Provides CRUD operations for Client objects using SQLAlchemy.
"""
from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client import ClientCreate

def get_all(db: Session):
    """
    Retrieve all client records from the database.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Client]: List of all clients.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    return db.query(Client).all()

def get_by_id(db: Session, kliento_id: int):
    """
    Retrieve a client by their unique ID.

    Args:
        db (Session): SQLAlchemy session.
        kliento_id (int): Client ID.

    Returns:
        Client or None: Client object if found, otherwise None.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    return db.query(Client).filter(Client.kliento_id == kliento_id).first()

def create(db: Session, client: ClientCreate):
    """
    Create a new client record in the database.

    Args:
        db (Session): SQLAlchemy session.
        client (ClientCreate): Pydantic schema with client data.

    Returns:
        Client: The created client object.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def delete(db: Session, kliento_id: int):
    """
    Delete a client record from the database.

    Args:
        db (Session): SQLAlchemy session.
        kliento_id (int): Client ID.

    Returns:
        bool: True if deleted successfully, False if client not found.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    db_client = get_by_id(db, kliento_id)
    if db_client:
        db.delete(db_client)
        db.commit()
        return True
    return False
