from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.repositories import employee as employee_repo
from app.schemas.employee import EmployeeOut
from app.api.deps import get_current_user, get_db
from app.schemas.employee import EmployeeUpdate, EmployeeOut
from app.services.auth_service import get_password_hash

router = APIRouter()

@router.get("/", response_model=list[EmployeeOut])
def get_employees(db: Session = Depends(get_db)):
    return employee_repo.get_all(db)

@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = employee_repo.get_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, data: EmployeeUpdate, db: Session = Depends(get_db)):
    updates = data.dict(exclude_unset=True)

    if "slaptazodis" in updates:
        updates["slaptazodis"] = get_password_hash(updates["slaptazodis"])

    updated = employee_repo.update(db, employee_id, updates)

    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = employee_repo.delete(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}