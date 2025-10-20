"""
app/api/v1/endpoints/client_support.py

API endpoints for client support requests management.

Author: Ivan Bruner <ivan.bruner@stud.viko.lt>

Description:
    Implements RESTful API routes for client support requests:
    create, retrieve, update (answer), and list unanswered requests.
    HATEOAS links are included in all responses for better API navigation.
"""
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.client_support import ClientSupportCreate, ClientSupportBase, ClientSupportOut, ClientSupportUpdate
from app.repositories import client_support
from app.api.deps import get_current_user
from datetime import datetime, timedelta
from app.models.client_support import ClientSupport

from app.api.permissions import require_perm, Perm

router = APIRouter(
    prefix="/support",
    tags=["Client Support"],
    dependencies=[Depends(get_current_user)]
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

@router.get(
    "/overdue",
    response_model=list[ClientSupportOut],
    operation_id="getOverdueSupports",
    dependencies=[Depends(require_perm(Perm.VIEW))]
)
def get_overdue_supports(
    hours: int = Query(24, ge=1, le=7*24, description="Hours since creation to consider a ticket overdue"),
    db: Session = Depends(get_db),
):
    """
    Retrieve overdue (unanswered) client support requests older than the given number of hours.

    A ticket is considered overdue if:
      1) It has no answer (atsakymas is NULL), and
      2) pateikimo_data < now - hours
    """
    if hours <= 0:
        raise HTTPException(status_code=400, detail="`hours` must be positive.")

    threshold = datetime.utcnow() - timedelta(hours=hours)

    # Būtiniausi laukai pagal tavo DB
    q = db.query(ClientSupport).filter(
        ClientSupport.atsakymas.is_(None),
        ClientSupport.pateikimo_data < threshold
    )

    # Jei turi statuso lauką – gali papildomai filtruoti „atviras“:
    # if hasattr(ClientSupport, "statusas"):
    #     q = q.filter(ClientSupport.statusas.in_(["OPEN", "PENDING", "NEATSAKYTA"]))

    items = q.order_by(ClientSupport.pateikimo_data.asc()).all()

    return [
        {
            **item.__dict__,
            "links": build_support_links(item)
        }
        for item in items
    ]


@router.post("/", response_model=ClientSupportOut, operation_id="createSupport", 
             dependencies=[Depends(require_perm(Perm.EDIT))])

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

@router.get("/", response_model=list[ClientSupportOut], operation_id="getAllSupports",
            dependencies=[Depends(require_perm(Perm.VIEW))])
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

@router.get("/unanswered", response_model=list[ClientSupportOut], operation_id="getUnansweredSupports",
            dependencies=[Depends(require_perm(Perm.VIEW))])
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

@router.get("/{uzklausos_id}", response_model=ClientSupportOut, operation_id="getSupport",
            dependencies=[Depends(require_perm(Perm.VIEW))])
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

@router.patch("/{uzklausos_id}", response_model=ClientSupportOut, operation_id="answerToSupport",
              dependencies=[Depends(require_perm(Perm.EDIT))])
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