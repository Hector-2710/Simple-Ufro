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
        
        start_cache = time.time()
        cached_data = await cache.get(key)
        end_cache = time.time()
        
        if cached_data:
            print(f"⚡ CACHE HIT for {key} | Time: {end_cache - start_cache:.4f}s")
            return [GradeRead(**item) for item in cached_data]

        start_db = time.time()
        statement = select(Grade).where(Grade.student_id == student_id).options(selectinload(Grade.subject))
        result = await session.execute(statement)
        grades = result.scalars().all()
        end_db = time.time()
        
        print(f"🐢 DB QUERY for {key} | Time: {end_db - start_db:.4f}s")
        
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
        sub_query = select(Grade.subject_id).where(Grade.student_id == student_id).distinct()
        statement = select(Subject).where(col(Subject.id).in_(sub_query))
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_student_schedule(session: AsyncSession, student_id: UUID) -> List[ScheduleRead]:
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
            
        return dtos

academic_service = AcademicService()
