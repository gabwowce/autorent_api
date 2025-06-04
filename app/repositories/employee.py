"""
app/repositories/employee.py

Repository functions for Employee entity database operations.

Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>

Description:
    Provides CRUD operations and utility queries for Employee objects using SQLAlchemy.
"""
from sqlalchemy.orm import Session
from app.models.employee import Employee

def get_by_email(db: Session, email: str):
    """
    Retrieve an employee by their email address.

    Args:
        db (Session): SQLAlchemy session.
        email (str): Employee email address.

    Returns:
        Employee or None: Employee object if found, otherwise None.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    return db.query(Employee).filter(Employee.el_pastas == email).first()


def get_by_id(db: Session, darbuotojo_id: int):
    """
    Retrieve an employee by their unique ID.

    Args:
        db (Session): SQLAlchemy session.
        darbuotojo_id (int): Employee ID.

    Returns:
        Employee or None: Employee object if found, otherwise None.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    return db.query(Employee).filter(Employee.darbuotojo_id == darbuotojo_id).first()

def create_employee(db: Session, data: dict):
    """
    Create a new employee record in the database.

    Args:
        db (Session): SQLAlchemy session.
        data (dict): Dictionary with employee data.

    Returns:
        Employee: The created employee object.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    naujas = Employee(**data)
    db.add(naujas)
    db.commit()
    db.refresh(naujas)
    return naujas

def get_all(db: Session):
    """
    Retrieve all employee records from the database.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Employee]: List of all employees.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    return db.query(Employee).all()

def update(db: Session, darbuotojo_id: int, updates: dict):
    """
    Update employee record.

    Args:
        db (Session): SQLAlchemy session.
        darbuotojo_id (int): Employee ID.
        updates (dict): Fields to update.

    Returns:
        Employee or None: Updated employee object or None if not found.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    employee = db.query(Employee).filter(Employee.darbuotojo_id == darbuotojo_id).first()
    if not employee:
        return None
    for key, value in updates.items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee

def delete(db: Session, darbuotojo_id: int):
    """
    Delete employee record.

    Args:
        db (Session): SQLAlchemy session.
        darbuotojo_id (int): Employee ID.

    Returns:
        True if deleted, None if not found.

    Author: Astijus Grinevičius <astijus.grinevicius@stud.viko.lt>
    """
    employee = db.query(Employee).filter(Employee.darbuotojo_id == darbuotojo_id).first()
    if not employee:
        return False
    db.delete(employee)
    db.commit()
    return True
