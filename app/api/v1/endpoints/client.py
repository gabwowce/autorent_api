from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas import client as schemas_client
from app.schemas import order as schemas_order

from app.repositories import client as repo
from utils.hateoas import generate_links

router = APIRouter(
    prefix="/clients",  
)

@router.get("/", response_model=list[schemas_client.ClientOut], operation_id="getAllClients")
def get_all_clients(db: Session = Depends(get_db)):
    clients = repo.get_all(db)
    return [
        {
            **client.__dict__,
            "links": generate_links("clients", client.kliento_id, ["update", "delete"])
        }
        for client in clients
    ]

@router.get("/{kliento_id}", response_model=schemas_client.ClientOut, operation_id="getClientById")
def get_client(kliento_id: int, db: Session = Depends(get_db)):
    client = repo.get_by_id(db, kliento_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return {
        **client.__dict__,
        "links": generate_links("clients", client.kliento_id, ["update", "delete"])
    }

@router.post("/", response_model=schemas_client.ClientOut, operation_id="createClient")
def create_client(client: schemas_client.ClientCreate, db: Session = Depends(get_db)):
    created = repo.create(db, client)
    return {
        **created.__dict__,
        "links": generate_links("clients", created.kliento_id, ["update", "delete"])
    }

@router.delete("/{kliento_id}", operation_id="deleteClient")
def delete_client(kliento_id: int, db: Session = Depends(get_db)):
    success = repo.delete(db, kliento_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"ok": True}


@router.get("/{kliento_id}/orders", response_model=list[schemas_order.OrderOut], operation_id="getClientOrder")
def get_client_orders(kliento_id: int, db: Session = Depends(get_db)):
    orders = repo.get_by_client_id(db, kliento_id)
    return [
        {
            **order.__dict__,
            "links": [
                {"rel": "self", "href": f"/orders/{order.uzsakymo_id}"},
                {"rel": "car", "href": f"/cars/{order.automobilio_id}"},
                {"rel": "delete", "href": f"/orders/{order.uzsakymo_id}"}
            ]
        }
        for order in orders
    ]
