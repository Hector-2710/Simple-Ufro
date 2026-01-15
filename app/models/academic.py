from typing import Optional, List
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, time
import uuid

class SubjectBase(SQLModel):
    code: str = Field(index=True, unique=True) 
    name: str
    credits: int
    description: Optional[str] = None

class Subject(SubjectBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    
    grades: List["Grade"] = Relationship(back_populates="subject")
    schedules: List["Schedule"] = Relationship(back_populates="subject")

class GradeBase(SQLModel):
    value: float 
    weight: float = 1.0 
    evaluation_name: str 
    evaluation_date: Optional[datetime] = None

class Grade(GradeBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    
    student_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    subject_id: uuid.UUID = Field(foreign_key="subject.id", index=True)
    
    subject: Subject = Relationship(back_populates="grades")


class DayOfWeek(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class ScheduleBase(SQLModel):
    day: str 
    start_time: time
    end_time: time
    classroom: str 

class Schedule(ScheduleBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    
    subject_id: uuid.UUID = Field(foreign_key="subject.id")
    
    subject: Subject = Relationship(back_populates="schedules")
