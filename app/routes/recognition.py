from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import tempfile
import os

from app.database.db import get_db
from app.models.employee import Employee
from app.services.face_service import recognize_face

router = APIRouter()


@router.post("/recognize")
async def recognize(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    temp.write(await file.read())
    temp.close()

    try:

        name, score = recognize_face(temp.name)

        if name is None:

            return {
                "success": False,
                "message": "Unknown Face"
            }

        employee = db.query(Employee).filter(
            Employee.employee_id == name
        ).first()

        if employee is None:

            return {
                "success": False,
                "message": "Employee Not Found"
            }

        return {

            "success": True,

            "employee": {

                "employee_id": employee.employee_id,
                "full_name": employee.full_name,
                "department": employee.department,
                "designation": employee.designation,
                "email": employee.email,
                "phone": employee.phone,
                "photo_url": employee.photo

            },

            "confidence": float(score)

        }

    finally:
        os.remove(temp.name)