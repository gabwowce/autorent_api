"""
app/repositories/client_support.py

Repository functions for ClientSupport entity database operations.

Author: Ivan Bruner <ivan.bruner@stud.viko.lt>

Description:
    Provides CRUD operations and utility queries for client support requests using SQLAlchemy.
"""
from sqlalchemy.orm import Session
from app.models import client_support
from app.models.client_support import ClientSupport
from app.schemas.client_support import ClientSupportCreate, ClientSupportUpdate
from datetime import datetime

def create_support_request(db: Session, support_data: ClientSupportCreate):
    """
    Create a new client support request.

    Args:
        db (Session): SQLAlchemy session.
        support_data (ClientSupportCreate): Pydantic schema with support request data.

    Returns:
        ClientSupport: The created client support object.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    data = support_data.dict()
    data.pop("pateikimo_data", None)
    db_support = client_support.ClientSupport(
        **data,
        pateikimo_data=datetime.utcnow()
    )
    db.add(db_support)
    db.commit()
    db.refresh(db_support)
    return db_support

def get_all_support_requests(db: Session):
    """
    Retrieve all client support requests from the database.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[ClientSupport]: List of all support requests.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    return db.query(client_support.ClientSupport).all()

def get_support_request_by_id(db: Session, uzklausos_id: int):
    """
    Retrieve a client support request by its unique ID.

    Args:
        db (Session): SQLAlchemy session.
        uzklausos_id (int): Support request ID.

    Returns:
        ClientSupport or None: Support request object if found, otherwise None.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    return db.query(client_support.ClientSupport).filter_by(uzklausos_id=uzklausos_id).first()

def update_support_request(db: Session, uzklausos_id: int, data: ClientSupportUpdate):
    """
    Update an existing client support request.

    Args:
        db (Session): SQLAlchemy session.
        uzklausos_id (int): Support request ID.
        data (ClientSupportUpdate): Pydantic schema with updated fields.

    Returns:
        ClientSupport or None: Updated support request if found, otherwise None.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    support = db.query(ClientSupport).filter(ClientSupport.uzklausos_id == uzklausos_id).first()
    if not support:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(support, key, value)
    db.commit()
    db.refresh(support)
    return support
    
def get_unanswered_requests(db: Session):
    """
    Retrieve all client support requests without an answer.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[ClientSupport]: List of unanswered support requests.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    return db.query(ClientSupport).filter(ClientSupport.atsakymas == None).all()
