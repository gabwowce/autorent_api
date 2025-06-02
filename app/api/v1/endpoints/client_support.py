"""
app/api/v1/endpoints/client_support.py

API endpoints for client support requests management.

Author: Ivan Bruner <ivan.bruner@stud.viko.lt>

Description:
    Implements RESTful API routes for client support requests:
    create, retrieve, update (answer), and list unanswered requests.
    HATEOAS links are included in all responses for better API navigation.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.client_support import ClientSupportCreate, ClientSupportOut, ClientSupportUpdate
from app.repositories import client_support

router = APIRouter(
    prefix="/support",
    tags=["Client Support"]
)

def build_support_links(support) -> list[dict]:
    """
    Build HATEOAS links for a client support request.

    Args:
        support: ClientSupport SQLAlchemy model instance.

    Returns:
        list[dict]: List of link dictionaries for navigation.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    return [
        {"rel": "self", "href": f"/support/{support.uzklausos_id}"},
        {"rel": "client", "href": f"/clients/{support.kliento_id}"},
        {"rel": "employee", "href": f"/employees/{support.darbuotojo_id}"},
        {"rel": "answer", "href": f"/support/{support.uzklausos_id}"},
        {"rel": "delete", "href": f"/support/{support.uzklausos_id}"}
    ]

@router.post("/", response_model=ClientSupportOut, operation_id="createSupport")
def create_support(support: ClientSupportCreate, db: Session = Depends(get_db)):
    """
    Create a new client support request.

    Args:
        support (ClientSupportCreate): Request body.
        db (Session): SQLAlchemy session.

    Returns:
        ClientSupportOut: Created support request with HATEOAS links.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    created = client_support.create_support_request(db, support)
    return {
        **created.__dict__,
        "links": build_support_links(created)
    }

@router.get("/", response_model=list[ClientSupportOut], operation_id="getAllSupports")
def get_all_supports(db: Session = Depends(get_db)):
    """
    Retrieve all client support requests.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        list[ClientSupportOut]: List of all support requests with HATEOAS links.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    items = client_support.get_all_support_requests(db)
    return [
        {
            **item.__dict__,
            "links": build_support_links(item)
        }
        for item in items
    ]

@router.get("/{uzklausos_id}", response_model=ClientSupportOut, operation_id="getSupport")
def get_support(uzklausos_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific client support request by ID.

    Args:
        uzklausos_id (int): Support request ID.
        db (Session): SQLAlchemy session.

    Returns:
        ClientSupportOut: Requested support with HATEOAS links.

    Raises:
        HTTPException: If support request not found.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    support = client_support.get_support_request_by_id(db, uzklausos_id)
    if not support:
        raise HTTPException(status_code=404, detail="Support request not found")
    return {
        **support.__dict__,
        "links": build_support_links(support)
    }

@router.patch("/{uzklausos_id}", response_model=ClientSupportOut, operation_id="answerToSupport")
def answer_to_support(uzklausos_id: int, data: ClientSupportUpdate, db: Session = Depends(get_db)):
    """
    Answer to an existing client support request.

    Args:
        uzklausos_id (int): Support request ID.
        data (ClientSupportUpdate): Update payload.
        db (Session): SQLAlchemy session.

    Returns:
        ClientSupportOut: Updated support request with HATEOAS links.

    Raises:
        HTTPException: If support request not found.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    updated = client_support.update_support_request(db, uzklausos_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Support request not found")
    return {
        **updated.__dict__,
        "links": build_support_links(updated)
    }

@router.get("/unanswered", response_model=list[ClientSupportOut], operation_id="getUnansweredSupports")
def get_unanswered_supports(db: Session = Depends(get_db)):
    """
    Retrieve all unanswered client support requests.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        list[ClientSupportOut]: List of unanswered support requests with HATEOAS links.

    Author: Ivan Bruner <ivan.bruner@stud.viko.lt>
    """
    items = client_support.get_unanswered_requests(db)
    return [
        {
            **item.__dict__,
            "links": build_support_links(item)
        }
        for item in items
    ]
