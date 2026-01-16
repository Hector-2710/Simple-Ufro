from typing import List, Any
from uuid import UUID
from sqlmodel import select, col
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.academic import Subject, Grade, Schedule
from app.models.user import User

class AcademicService:
    @staticmethod
    async def get_all_subjects(session: AsyncSession) -> List[Subject]:
        statement = select(Subject)
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_student_grades(session: AsyncSession, student_id: UUID) -> List[Grade]:
        # Return grades with subject data loaded
        statement = select(Grade).where(Grade.student_id == student_id).options(selectinload(Grade.subject))
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_student_subjects(session: AsyncSession, student_id: UUID) -> List[Subject]:
        # Logic: Get subjects where the student has at least one grade (Active Subjects)
        sub_query = select(Grade.subject_id).where(Grade.student_id == student_id).distinct()
        
        statement = select(Subject).where(col(Subject.id).in_(sub_query))
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_student_schedule(session: AsyncSession, student_id: UUID) -> List[Schedule]:
        # Logic: Get schedules for subjects where the student has at least one grade (Active Subjects)
        
        sub_query = select(Grade.subject_id).where(Grade.student_id == student_id).distinct()
        
        statement = select(Schedule).where(col(Schedule.subject_id).in_(sub_query)).options(selectinload(Schedule.subject))
        result = await session.execute(statement)
        return result.scalars().all()

academic_service = AcademicService()
