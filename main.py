from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.employee import router as employee_router
from app.routes.attendance import router as attendance_router
from app.routes.camera import router as camera_router
from app.routes.dashboard import router as dashboard_router
from app.routes import idcard_detection

# Import face loader
from app.services.face_service import load_faces

app = FastAPI(title="Face Detection Attendance System")

# Load employee face embeddings at startup
@app.on_event("startup")
def startup_event():
    print("Loading employee face database...")
    load_faces()
    print("Employee face database loaded successfully.")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(employee_router, prefix="/employees", tags=["Employees"])
app.include_router(attendance_router, prefix="/attendance", tags=["Attendance"])
app.include_router(camera_router, prefix="/camera", tags=["Camera"])
app.include_router(idcard_detection.router, prefix="/api", tags=["ID Card Detection"])

@app.get("/")
def home():
    return {
        "message": "Face Detection API Running"
    }