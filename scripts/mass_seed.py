import asyncio
import sys
import os

# Add project root to sys.path before app imports
sys.path.append(os.getcwd())

import random
from datetime import datetime, time, timedelta
from faker import Faker
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.user import User, Role
from app.models.academic import Subject, Grade, Schedule
from app.core import security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

_DATABASE_URL = os.getenv("DATABASE_URL")

if _DATABASE_URL:
    engine = create_async_engine(_DATABASE_URL, future=True)
else:
    from app.db.session import engine

fake = Faker()

async def mass_seed_data(count: int = 2000, reset_db: bool = False):
    print(f"🚀 Starting mass data seeding ({count} students)...")
    
    if reset_db:
        print("🧹 Resetting database schema...")
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    password_hash = security.get_password_hash("password123")
    
    async with async_session() as session:
        print("📚 Generating subjects...")
        subject_names = [
            "Álgebra Lineal", "Cálculo I", "Cálculo II", "Física Mecánica", 
            "Física Electromagnetismo", "Programación I", "Programación II", 
            "Estructuras de Datos", "Bases de Datos", "Sistemas Operativos",
            "Redes de Computadores", "Ingeniería de Software", "Inteligencia Artificial",
            "Ética Profesional", "Gestión de Proyectos"
        ]
        
        subjects = []
        for name in subject_names:
            code = f"{name[:3].upper()}{random.randint(100, 999)}"
            subject = Subject(
                code=code,
                name=name,
                credits=random.randint(2, 6),
                description=fake.paragraph(nb_sentences=2)
            )
            session.add(subject)
            subjects.append(subject)
        
        await session.commit()
        for s in subjects: await session.refresh(s)
        
        print("📅 Generating schedules...")
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        classrooms = ["A-101", "A-102", "B-201", "B-205", "Lab-1", "Lab-Computacion"]
        
        for subject in subjects:
            num_classes = random.randint(1, 2)
            for _ in range(num_classes):
                day = random.choice(days)
                start_hour = random.randint(8, 17)
                start_time = time(start_hour, 30)
                end_time = time(start_hour + 1, 30)
                
                schedule = Schedule(
                    subject_id=subject.id,
                    day=day,
                    start_time=start_time,
                    end_time=end_time,
                    classroom=random.choice(classrooms)
                )
                session.add(schedule)
        await session.commit()

        print(f"👤 Generating {count} students and their grades...")
        
        test_student = User(
            email="student1@ufro.cl",
            username="student1",
            full_name="Test Student",
            hashed_password=password_hash,
            role=Role.STUDENT
        )
        session.add(test_student)
        await session.flush()
        
        # Enroll test_student in some subjects
        for sub in random.sample(subjects, 3):
            for i in range(2):
                session.add(Grade(
                    student_id=test_student.id,
                    subject_id=sub.id,
                    value=6.0,
                    weight=0.5,
                    evaluation_name=f"Test Eval {i+1}",
                    evaluation_date=datetime.now()
                ))

        chunk_size = 100
        for i in range(0, count, chunk_size):
            actual_chunk = min(chunk_size, count - i)
            for _ in range(actual_chunk):
                username = f"{fake.user_name()}{random.randint(1, 100000)}"
                student = User(
                    email=f"{username}@ufro.cl",
                    username=username,
                    full_name=fake.name(),
                    hashed_password=password_hash,
                    role=Role.STUDENT
                )
                session.add(student)
                await session.flush() 
                
                enrolled_subjects = random.sample(subjects, random.randint(3, 6))
                for sub in enrolled_subjects:
                    for g_idx in range(random.randint(2, 4)):
                        grade = Grade(
                            student_id=student.id,
                            subject_id=sub.id,
                            value=round(random.uniform(1.0, 7.0), 1),
                            weight=0.25,
                            evaluation_name=f"Evaluation {g_idx + 1}",
                            evaluation_date=datetime.now() - timedelta(days=random.randint(1, 100))
                        )
                        session.add(grade)
            
            await session.commit()
            print(f"   -> Progress: {i + actual_chunk}/{count} students added.")

    print(f"✅ Finished! Successfully added {count} students and academic data.")

if __name__ == "__main__":
    count_to_seed = 2000
    reset_db = False
    
    if "--reset" in sys.argv:
        reset_db = True
        sys.argv.remove("--reset")
        
    if len(sys.argv) > 1:
        try:
            count_to_seed = int(sys.argv[1])
        except ValueError:
            pass
            
    asyncio.run(mass_seed_data(count_to_seed, reset_db))

