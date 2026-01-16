from typing import Optional
from datetime import datetime, time
from sqlmodel import SQLModel 
from uuid import UUID

class SubjectRead(SQLModel):
    id: UUID
    code: str
    name: str
    credits: int
    description: Optional[str] = None

class GradeRead(SQLModel):
    id: UUID
    value: float
    weight: float
    evaluation_name: str
    evaluation_date: Optional[datetime] = None
    subject_name: str
    subject_code: str

class ScheduleRead(SQLModel):
    id: UUID
    day: str
    start_time: time
    end_time: time
    classroom: str
    subject_name: str
    subject_code: str
