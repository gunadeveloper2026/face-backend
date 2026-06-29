from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.employee import Employee
from app.models.attendance import Attendance

router = APIRouter()


@router.get("/")
def camera_dashboard(
    db: Session = Depends(get_db)
):
    try:

        total_employees = (
            db.query(Employee)
            .count()
        )

        present_count = (
            db.query(Attendance)
            .filter(
                Attendance.status == "Present"
            )
            .count()
        )

        absent_count = (
            total_employees - present_count
        )

        faces_detected = (
            db.query(Attendance)
            .count()
        )

        last_record = (
            db.query(Attendance)
            .order_by(
                Attendance.id.desc()
            )
            .first()
        )

        logs = (
            db.query(Attendance)
            .order_by(
                Attendance.id.desc()
            )
            .limit(10)
            .all()
        )

        attendance_logs = []

        for log in logs:

            attendance_logs.append(
                {
                    "employeeId":
                        log.employee_id,

                    "name":
                        log.employee.full_name
                        if log.employee
                        else "Unknown",

                    "time":
                        log.check_in_time.strftime(
                            "%I:%M %p"
                        )
                        if log.check_in_time
                        else "N/A",

                    "status":
                        log.status
                }
            )

        return {

            "cameraActive": True,

            "employeesPresent":
                present_count,

            "employeesAbsent":
                absent_count,

            "facesDetected":
                faces_detected,

            "accuracy": 98,

            "recognitionStatus":
                "Running Successfully",

            "databaseStatus":
                "Connected",

            "lastDetected":
                last_record.employee_id
                if last_record
                else "N/A",

            "detectionTime":
                last_record.check_in_time.strftime(
                    "%I:%M:%S %p"
                )
                if last_record
                and last_record.check_in_time
                else "N/A",

            "logs":
                attendance_logs
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }