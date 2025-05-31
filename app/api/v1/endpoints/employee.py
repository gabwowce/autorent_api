from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.repositories import employee as employee_repo
from app.schemas.employee import EmployeeOut, EmployeeUpdate
from app.api.deps import get_db
from app.services.auth_service import get_password_hash
from utils.hateoas import generate_links

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@router.get("/", response_model=list[EmployeeOut], operation_id="getAllEmployees")
def get_employees(db: Session = Depends(get_db)):
    employees = employee_repo.get_all(db)
    return [
        {
            **emp.__dict__,
            "links": generate_links("employees", emp.darbuotojo_id, ["update", "delete"])
        }
        for emp in employees
    ]

@router.get("/{employee_id}", response_model=EmployeeOut, operation_id="getEmployee")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = employee_repo.get_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {
        **employee.__dict__,
        "links": generate_links("employees", employee.darbuotojo_id, ["update", "delete"])
    }

@router.put("/{employee_id}", response_model=EmployeeOut, operation_id="updateEmployee")
def update_employee(employee_id: int, data: EmployeeUpdate, db: Session = Depends(get_db)):
    updates = data.dict(exclude_unset=True)

    if "slaptazodis" in updates:
        updates["slaptazodis"] = get_password_hash(updates["slaptazodis"])

    updated = employee_repo.update(db, employee_id, updates)

    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {
        **updated.__dict__,
        "links": generate_links("employees", updated.darbuotojo_id, ["update", "delete"])
    }

@router.delete("/{employee_id}", operation_id="deleteEmployee")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = employee_repo.delete(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}
