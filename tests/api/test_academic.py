import pytest
from httpx import AsyncClient
from app.models.user import User, Role
from app.models.academic import Subject, Grade, Schedule
import uuid
from datetime import time
from app.core import security

@pytest.mark.asyncio
async def test_read_my_academic_data(client: AsyncClient, db_session):
    student_id = uuid.uuid4()
    student = User(
        id=student_id,
        email="student@example.com",
        username="student",
        full_name="Student User",
        hashed_password=security.get_password_hash("password123"),
        role=Role.STUDENT,
        is_active=True
    )
    db_session.add(student)
    
    subject_id = uuid.uuid4()
    subject = Subject(
        id=subject_id,
        code="INF-123",
        name="Computer Science 101",
        credits=5
    )
    db_session.add(subject)
    
    grade = Grade(
        id=uuid.uuid4(),
        value=5.5,
        evaluation_name="Exam 1",
        student_id=student_id,
        subject_id=subject_id
    )
    db_session.add(grade)
    
    schedule = Schedule(
        id=uuid.uuid4(),
        day="Monday",
        start_time=time(8, 0),
        end_time=time(10, 0),
        classroom="A101",
        subject_id=subject_id
    )
    db_session.add(schedule)
    await db_session.commit()
    
    login_response = await client.post("/api/v1/login/access-token", data={"username": "student", "password": "password123"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = await client.get("/api/v1/academic/subjects", headers=headers)
    assert response.status_code == 200
    subjects = response.json()
    assert len(subjects) == 1
    assert subjects[0]["code"] == "INF-123"
    
    response = await client.get("/api/v1/academic/grades", headers=headers)
    assert response.status_code == 200
    grades = response.json()
    assert len(grades) == 1
    assert grades[0]["value"] == 5.5
    
    response = await client.get("/api/v1/academic/schedule", headers=headers)
    assert response.status_code == 200
    schedules = response.json()
    assert len(schedules) == 1
    assert schedules[0]["subject_name"] == "Computer Science 101"
