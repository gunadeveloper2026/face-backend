from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.database.db import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100))
    department = Column(String(50))
    designation = Column(String(100))
    phone = Column(String(20))
    face_image = Column(String(255))
    face_encoding = Column(Text)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    status = Column(String(20), default="Active")