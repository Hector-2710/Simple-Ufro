from typing import Any, List
from fastapi import APIRouter
from app.api.deps import SessionDep, GetCurrentUser
from app.services.academic_service import academic_service
from app.schemas.academic import SubjectRead, GradeRead, ScheduleRead

router = APIRouter()

@router.get("/subjects", response_model=List[SubjectRead])
async def read_my_subjects(session: SessionDep, current_user: GetCurrentUser) -> Any:
    """
    Retrieve subjects for the current user (Enrolled).
    """
    return await academic_service.get_student_subjects(session, current_user.id)

@router.get("/grades", response_model=List[GradeRead])
async def read_my_grades(session: SessionDep, current_user: GetCurrentUser) -> Any:
    """
    Retrieve my grades.
    """
    return await academic_service.get_student_grades(session, current_user.id)

@router.get("/schedule", response_model=List[ScheduleRead])
async def read_my_schedule(session: SessionDep, current_user: GetCurrentUser) -> Any:
    """
    Retrieve my weekly schedule.
    """
    return await academic_service.get_student_schedule(session, current_user.id)
