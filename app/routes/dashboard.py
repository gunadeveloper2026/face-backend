from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def dashboard():
    return {
        "totalEmployees": 150,
        "presentToday": 120,
        "absentToday": 30,
        "facesDetected": 245,
        "attendancePercentage": 80,
        "accuracy": 98.7,
        "logs": [
            {
                "id": "EMP001",
                "name": "John Doe",
                "dept": "IT",
                "time": "09:01 AM",
                "status": "Present"
            },
            {
                "id": "EMP002",
                "name": "Jane Smith",
                "dept": "HR",
                "time": "09:05 AM",
                "status": "Present"
            },
            {
                "id": "EMP003",
                "name": "Robert",
                "dept": "Finance",
                "time": "09:12 AM",
                "status": "Present"
            }
        ]
    }