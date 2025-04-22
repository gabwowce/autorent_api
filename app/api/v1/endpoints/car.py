from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.repositories import car as car_repo
from app.schemas.car import CarOut, CarCreate, CarUpdate, CarStatusUpdate

router = APIRouter()

@router.get("/", response_model=list[CarOut])
def get_all_cars(db: Session = Depends(get_db)):
    return car_repo.get_all(db)

@router.get("/{car_id}", response_model=CarOut)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = car_repo.get_by_id(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.post("/", response_model=CarOut)
def create_car(data: CarCreate, db: Session = Depends(get_db)):
    return car_repo.create(db, data.dict())

@router.put("/{car_id}", response_model=CarOut)
def update_car(car_id: int, data: CarUpdate, db: Session = Depends(get_db)):
    updated = car_repo.update(db, car_id, data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Car not found")
    return updated

@router.delete("/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    deleted = car_repo.delete(db, car_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted successfully"}

@router.patch("/{car_id}/status")
def update_car_status(car_id: int, data: CarStatusUpdate, db: Session = Depends(get_db)):
    updated = car_repo.update_status(db, car_id, data.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car status updated successfully"}