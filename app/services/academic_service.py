from typing import List
import time
from uuid import UUID
from sqlmodel import select, col
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.academic import Subject, Grade, Schedule
from app.core.cache import cache
from app.schemas.academic import GradeRead, ScheduleRead

class AcademicService:
    @staticmethod
    async def get_student_grades(session: AsyncSession, student_id: UUID) -> List[GradeRead]:
        key = f"grades:{student_id}"
        cached_data = await cache.get(key)
        if cached_data:
            return [GradeRead(**item) for item in cached_data]

        statement = select(Grade).where(Grade.student_id == student_id).options(selectinload(Grade.subject))
        result = await session.execute(statement)
        grades = result.scalars().all()
        
        dtos = [
            GradeRead(
                id=g.id,
                value=g.value,
                weight=g.weight,
                evaluation_name=g.evaluation_name,
                evaluation_date=g.evaluation_date,
                subject_name=g.subject.name,
                subject_code=g.subject.code
            ) for g in grades
        ]
        
        if dtos:
            await cache.set(key, [dto.model_dump(mode='json') for dto in dtos], ttl=300)
        
        return dtos

    @staticmethod
    async def get_student_subjects(session: AsyncSession, student_id: UUID) -> List[Subject]:
        key = f"subjects:{student_id}"
        
        cached_data = await cache.get(key)
        if cached_data:
            return [Subject.model_validate(item) for item in cached_data]

        sub_query = select(Grade.subject_id).where(Grade.student_id == student_id).distinct()
        statement = select(Subject).where(col(Subject.id).in_(sub_query))
        result = await session.execute(statement)
        subjects = result.scalars().all()
        
        if subjects:
            await cache.set(key, [s.model_dump(mode='json') for s in subjects], ttl=300)
            
        return subjects

    @staticmethod
    async def get_student_schedule(session: AsyncSession, student_id: UUID) -> List[ScheduleRead]:
        key = f"schedule:{student_id}"
        
        cached_data = await cache.get(key)
        if cached_data:
            return [ScheduleRead(**item) for item in cached_data]

        sub_query = select(Grade.subject_id).where(Grade.student_id == student_id).distinct()
        statement = select(Schedule).where(col(Schedule.subject_id).in_(sub_query)).options(selectinload(Schedule.subject))
        result = await session.execute(statement)
        schedules = result.scalars().all()
        
        dtos = [
            ScheduleRead(
                id=s.id,
                day=s.day,
                start_time=s.start_time,
                end_time=s.end_time,
                classroom=s.classroom,
                subject_name=s.subject.name,
                subject_code=s.subject.code
            ) for s in schedules
        ]
        
        if dtos:
            await cache.set(key, [dto.model_dump(mode='json') for dto in dtos], ttl=300)
            
        return dtos

academic_service = AcademicService()
