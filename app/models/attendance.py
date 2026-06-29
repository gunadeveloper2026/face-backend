from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.database.db import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)

    employee_id = Column(
        String(20),
        ForeignKey("employees.employee_id")
    )

    attendance_date = Column(Date)

    check_in_time = Column(Time)

    status = Column(String(20))

    employee = relationship(
        "Employee",
        lazy="joined"
    )