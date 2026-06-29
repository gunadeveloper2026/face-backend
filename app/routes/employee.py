from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException
)
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.employee import Employee

import os
import shutil

router = APIRouter()

UPLOAD_DIR = "app/static/employees"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()

    return [
        {
            "id": emp.id,
            "employee_id": emp.employee_id,
            "full_name": emp.full_name,
            "department": emp.department,
            "designation": emp.designation,
            "phone": emp.phone,
            "status": emp.status
        }
        for emp in employees
    ]


@router.post("/register")
async def register_employee(
    employee_id: str = Form(...),
    full_name: str = Form(...),
    department: str = Form(...),
    designation: str = Form(...),
    phone: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    existing_employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Employee ID already exists"
        )

    image_path = os.path.join(
        UPLOAD_DIR,
        f"{employee_id}.jpg"
    )

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(
            image.file,
            buffer
        )

    new_employee = Employee(
        employee_id=employee_id,
        full_name=full_name,
        department=department,
        designation=designation,
        phone=phone,
        status="Active"
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {
        "message": "Employee Registered Successfully",
        "employee": {
            "employee_id": employee_id,
            "full_name": full_name,
            "department": department
        }
    }


@router.get("/test")
def test():
    return {
        "message": "Employee Router Working"
    }