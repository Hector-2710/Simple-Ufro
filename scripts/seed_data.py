import asyncio
import sys
import os
from datetime import datetime, time, date

# Add the project root to the python path
sys.path.append(os.getcwd())

from sqlmodel import select, delete, SQLModel
from app.db.session import engine, init_db
from app.models.user import User, Role
from app.models.academic import Subject, Grade, Schedule
from app.core import security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async def seed_data():
    print("🌱 Starting data seeding...")
    
    # Init DB (ensure tables exist and schema is updated)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # 1. Clean up existing data (Optional: Be careful in Prod)
        print("🧹 Cleaning old data...")
        await session.execute(delete(Grade))
        await session.execute(delete(Schedule))
        await session.execute(delete(Subject))
        await session.execute(delete(User))
        await session.commit()
        
        # 2. Create Users
        print("👤 Creating users...")
        student_password = security.get_password_hash("password123")
        
        student1 = User(
            email="student@ufro.cl",
            username="student1",
            full_name="Juan Perez",
            hashed_password=student_password,
            role=Role.STUDENT
        )
        
        student2 = User(
            email="ana@ufro.cl",
            username="student2",
            full_name="Ana Garcia",
            hashed_password=student_password,
            role=Role.STUDENT
        )
        
        session.add(student1)
        session.add(student2)
        await session.commit()
        await session.refresh(student1)
        await session.refresh(student2)
        print(f"   -> Created student: {student1.email} (pass: password123)")
        print(f"   -> Created student: {student2.email} (pass: password123)")

        # 3. Create Subjects
        print("📚 Creating subjects...")
        algebra = Subject(
            code="MAT101",
            name="Álgebra Lineal",
            credits=5,
            description="Introducción al álgebra lineal y matrices."
        )
        fisica = Subject(
            code="FIS101",
            name="Física Mecánica",
            credits=4,
            description="Leyes de Newton y movimiento."
        )
        prog = Subject(
            code="INF101",
            name="Programación I",
            credits=6,
            description="Introducción a Python y algoritmos."
        )
        
        session.add(algebra)
        session.add(fisica)
        session.add(prog)
        await session.commit()
        
        # Refresh to get IDs
        await session.refresh(algebra)
        await session.refresh(fisica)
        await session.refresh(prog)

        # 4. Create Schedules
        print("📅 Creating schedules...")
        schedules = [
            Schedule(subject_id=algebra.id, day="Monday", start_time=time(8, 30), end_time=time(10, 0), classroom="A-101"),
            Schedule(subject_id=algebra.id, day="Wednesday", start_time=time(8, 30), end_time=time(10, 0), classroom="A-101"),
            Schedule(subject_id=fisica.id, day="Tuesday", start_time=time(14, 30), end_time=time(16, 0), classroom="Lab-2"),
            Schedule(subject_id=prog.id, day="Friday", start_time=time(10, 15), end_time=time(13, 0), classroom="Lab-Computacion")
        ]
        session.add_all(schedules)
        await session.commit()

        # 5. Create Grades (Only for Student 1 for now)
        print("📝 Assigning grades...")
        grades = [
            # Algebra Grades
            Grade(student_id=student1.id, subject_id=algebra.id, value=5.5, weight=0.3, evaluation_name="Certamen 1", evaluation_date=datetime(2025, 4, 15)),
            Grade(student_id=student1.id, subject_id=algebra.id, value=6.2, weight=0.3, evaluation_name="Certamen 2", evaluation_date=datetime(2025, 5, 20)),
            
            # Prog Grades
            Grade(student_id=student1.id, subject_id=prog.id, value=7.0, weight=0.2, evaluation_name="Tarea 1", evaluation_date=datetime(2025, 3, 25)),
            Grade(student_id=student1.id, subject_id=prog.id, value=6.8, weight=0.4, evaluation_name="Proyecto Semestral", evaluation_date=datetime(2025, 7, 5))
        ]
        session.add_all(grades)
        await session.commit()
        
    print("✅ Seed data created successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
