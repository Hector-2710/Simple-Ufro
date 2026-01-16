from typing import List
from uuid import UUID
from sqlmodel import select, col
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.academic import Subject, Grade, Schedule

class AcademicService:
    @staticmethod
    async def get_all_subjects(session: AsyncSession) -> List[Subject]:
        statement = select(Subject)
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_student_grades(session: AsyncSession, student_id: UUID) -> List[Grade]:
        statement = select(Grade).where(Grade.student_id == student_id).options(selectinload(Grade.subject))
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_student_subjects(session: AsyncSession, student_id: UUID) -> List[Subject]:
        sub_query = select(Grade.subject_id).where(Grade.student_id == student_id).distinct()
        statement = select(Subject).where(col(Subject.id).in_(sub_query))
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_student_schedule(session: AsyncSession, student_id: UUID) -> List[Schedule]:
        sub_query = select(Grade.subject_id).where(Grade.student_id == student_id).distinct()
        statement = select(Schedule).where(col(Schedule.subject_id).in_(sub_query)).options(selectinload(Schedule.subject))
        result = await session.execute(statement)
        return result.scalars().all()

academic_service = AcademicService()
