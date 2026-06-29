from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def attendance_list():
    return [
        {
            "id": "EMP001",
            "name": "John Doe",
            "department": "IT",
            "status": "Present",
            "checkIn": "09:02 AM",
            "date": "18-06-2026",
        },
        {
            "id": "EMP002",
            "name": "David",
            "department": "HR",
            "status": "Absent",
            "checkIn": "--",
            "date": "18-06-2026",
        },
        {
            "id": "EMP003",
            "name": "Robert",
            "department": "Finance",
            "status": "Late",
            "checkIn": "09:35 AM",
            "date": "18-06-2026",
        }
    ]